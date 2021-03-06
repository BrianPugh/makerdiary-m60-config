import board
import busio
import digitalio
import microcontroller
from adafruit_bus_device.i2c_device import I2CDevice


class IS31FL3733:
    def __init__(self, address=0x50, dev=None):
        self.address = address
        self._page = None
        self._buffer = bytearray(12 * 16 + 1)
        self._buffer[0] = 0
        self.pixels = memoryview(self._buffer)[1:]
        self.mode_mask = 0

        self.power = digitalio.DigitalInOut(microcontroller.pin.P1_04)
        self.power.direction = digitalio.Direction.OUTPUT
        self.power.value = 1

        if dev is None:
            dev = busio.I2C(board.SCL, board.SDA, frequency=400000)
        self.i2c = I2CDevice(dev, self.address)

        self.reset()
        self.setup()

        self.power.value = 0

    def page(self, n):
        if self._page is n:
            return
        self._page = n
        self.write(0xFE, 0xC5)
        self.write(0xFD, n)

    def reset(self):
        # read reset register (0x11) of page 3 to reset
        self.page(3)
        self.read(0x11)

    def setup(self):
        # configure 3 breathing modes
        self.page(3)
        self.write(2, (2 << 5) | (0 << 1))
        self.write(3, (2 << 5) | (3 << 1))
        self.write(4, (0 << 4))

        self.write(6, (2 << 5) | (0 << 1))
        self.write(7, (2 << 5) | (2 << 1))
        self.write(8, (0 << 4))

        self.write(0xA, (1 << 5) | (0 << 1))
        self.write(0xB, (1 << 5) | (1 << 1))
        self.write(0xC, (0 << 4))

        self.write(0, 1)
        self.write(0, 3)
        self.write(0xE, 0)

        self.set_brightness(128)

        self.page(0)
        self.write(0, [255] * 0x18)

    def set_brightness(self, n):
        n &= 0xFF
        self._brightness = n
        if not self.power.value:
            self.power.value = 1

        # Global Current Control register (0x01) of page 3
        self.page(3)
        self.write(1, n)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, n):
        self.set_brightness(n)

    def clear(self):
        pixels = self.pixels
        for i in range(192):
            pixels[i] = 0

    def pixel(self, i, r, g, b):
        """Set the pixel. It takes effect after calling update()"""
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        offset = row * 48 + col
        self.pixels[offset] = g
        self.pixels[offset + 16] = r
        self.pixels[offset + 32] = b

    def update_pixel(self, i, r, g, b):
        """Set the pixel and update"""
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        offset = row * 48 + col
        self.pixels[offset] = g
        self.pixels[offset + 16] = r
        self.pixels[offset + 32] = b
        self.power.value = 1
        self.page(1)
        self.write(offset, g)
        self.write(offset + 16, r)
        self.write(offset + 32, b)
        if not self.any():
            self.power.value = 0

    def update(self):
        self.power.value = 1
        self.page(1)
        with self.i2c:
            self.i2c.write(self._buffer)
        if not self.any():
            self.power.value = 0

    def any(self):
        """Check if any pixel is not zero"""
        if self.mode_mask > 0:
            return True
        for pixel in self.pixels:
            if pixel > 0:
                return True
        return False

    def write(self, register, value):
        if type(value) is int:
            with self.i2c:
                self.i2c.write(bytearray((register, value)))
        else:
            value.insert(0, register)
            buffer = bytearray(value)
            with self.i2c:
                self.i2c.write(buffer)

    def read(self, register):
        buffer = bytearray(1)
        with self.i2c:
            self.i2c.write_then_readinto(bytearray((register,)), buffer)
        return buffer[0]

    def set_mode(self, i, mode=2):
        self.power.value = 1
        self.page(2)
        row = i >> 4  # i // 16
        col = i & 15  # i % 16
        self.write(row * 48 + 32 + col, mode)
        if mode:
            self.mode_mask |= 1 << i
        else:
            self.mode_mask &= ~(1 << i)
            if not self.any():
                self.power.value = 0

    def open_pixels(self):
        # 18h ~ 2Fh LED Open Register
        self.page(0)
        buffer = bytearray(0x18)
        with self.i2c:
            self.i2c.write_then_readinto(bytearray((0x18,)), buffer)
        return buffer

    def short_pixels(self):
        # 30h ~ 47h LED Short Register
        self.page(0)
        buffer = bytearray(0x18)
        with self.i2c:
            self.i2c.write_then_readinto(bytearray((0x30,)), buffer)
        return buffer
