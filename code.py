import sys
import microcontroller
from keyboard import *
from time import sleep

MACRO_BATT = const(1)
MACRO_REPL = const(2)
MACRO_INSTALL_VIM = const(3)
MACRO_INSTALL_TMUX = const(4)
MACRO_ZPROFILE = const(5)
MACRO_RGB_VAL_INC = const(6)
MACRO_RGB_VAL_DEC = const(7)
MACRO_IPDB = const(8)
MACRO_TEST = const(9)
MACRO_SUSPEND_SHUTDOWN = const(10)
MACRO_PLT = const(11)

keyboard = Keyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)  # Primarily for keys missing on a 60%
L2 = LAYER_TAP(2)  # Primarily for advanced special functionality.
RCTRL_UP = MODS_TAP(MODS(RCTRL), UP)  # Tapping right control sends the "up" arrow

keyboard.keymap = (
    # layer 0
    (
        ESC,    1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,    Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        L1,     A,   S,   D,   F,   G,   H,   J,   K,   L, ';', '"',    ENTER,
        LSHIFT, Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',         RSHIFT,
        LCTRL, LGUI, LALT,          SPACE,            RALT,  L1,  L2,   RCTRL_UP
    ),

    # layer 1
    (
        '`',  F1,      F2,      F3,   F4,   F5,   F6,   F7,    F8,    F9,    F10,  F11, F12, DEL,
        ___, MACRO(MACRO_REPL),     ___,     ___, BOOT,  ___,  ___, PGUP,    UP,  PGDN, MACRO(MACRO_IPDB),  ___, ___, ___,
        ___, ___,   VOLDN,   VOLUP, MUTE, ___, HOME, LEFT,  DOWN, RIGHT, INSERT,  ___,      ___,
        ___, ___, BRGHTDN, BRGHTUP, ___,  MACRO(MACRO_BATT),  END,  MACRO(MACRO_PLT),   ___,   ___,    ___, ___,
        ___, ___,   ___,                   ___,                     ___,   ___,   ___,      ___
    ),

    # layer 2 (Advanced Special Functionality)
    (
        '`', BT1, BT2, BT3, BT4, BT5, BT6, BT7, BT8, BT9, BT0, MACRO(MACRO_RGB_VAL_DEC), MACRO(MACRO_RGB_VAL_INC), ___,
        ___, ___, ___, ___, ___, MACRO(MACRO_INSTALL_TMUX), ___, USB_TOGGLE, ___, ___, ___, ___, ___, ___,
        ___, ___, MACRO(MACRO_SUSPEND_SHUTDOWN), ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, MACRO(MACRO_ZPROFILE), ___, ___, MACRO(MACRO_INSTALL_VIM), BT_TOGGLE, ___, ___, ___, ___, MACRO(MACRO_TEST), ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # Blank layer for reference
    (
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)


def macro_handler_batt(dev, is_down, shift, ctrl):
    if is_down:
        level = battery_level()
        is_charging = battery_charge()
        if shift:
            dev.send_text("Battery Level: {}%".format(level))
        else:
            bars = int(round(level / 7.14))
            dev.backlight.off()
            for i in range(bars):
                if i == 0 and is_charging:
                    dev.backlight.pixel(i, 255, 0, 0)
                else:
                    dev.backlight.pixel(i, 0, 255, 0)

                dev.backlight.update()

                if i != bars - 1:
                    sleep(0.03)
    else:
        dev.backlight.set_mode(dev.backlight.mode)

def macro_handler_repl(dev, is_down, shift, ctrl):
    sys.exit()

def macro_handler_install_vim(dev, is_down, shift, ctrl):
    if not is_down:
        return
    dev.send_text((
        "git clone --recursive https://github.com/BrianPugh/vimrc.git ~/.vim_runtime"
        " && sh ~/.vim_runtime/install_awesome_vimrc.sh"
        " # Remember to run \"vim\" followed by \":PlugInstall\""
        ))

def macro_handler_install_tmux(dev, is_down, shift, ctrl):
    if not is_down:
        return
    dev.send_text((
        "git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm"
        " && wget -O ~/.tmux.conf https://gist.githubusercontent.com/BrianPugh/8b51fc7422c300e0caa9ec45841d5125/raw/9a6be775cc252bf7fdd6b764103535ef4799840a/tmux.conf"
        " && tmux source-file ~/.tmux.conf"
        ))

def macro_handler_zprofile(dev, is_down, shift, ctrl):
    if not is_down:
        return
    dev.send_text((
        'echo -e "\\n" >> ~/.zprofile'
        ' && wget https://gist.githubusercontent.com/BrianPugh/18e6d35e181de2a0371ce9986c448dbe/raw/68b50a6b1ebe7fc6cacfe3e28a8987526909edfc/.zprofile -O ->> ~/.zprofile'
        ))

def macro_handler_rgb_val_dec(dev, is_down, shift, ctrl):
    if not is_down:
        return
    if shift:
        dev.backlight.val -= 30
    else:
        dev.backlight.val -= 10
    if dev.backlight.val <= 0:
        dev.backlight.val = 0
        dev._backlight_off()
    dev.backlight.update()

def macro_handler_rgb_val_inc(dev, is_down, shift, ctrl):
    if not is_down:
        return
    if shift:
        dev.backlight.val += 30
    else:
        dev.backlight.val += 10
    if dev.backlight.val > 255:
        dev.backlight.val = 255
    dev.backlight.update()

def macro_handler_ipdb(dev, is_down, shift, ctrl):
    if not is_down:
        return
    dev.send_text((
        '\x1b'
        'o'
        'import ipdb; ipdb.set_trace()'
        '\x1b'
        ':w\n'
        ))

def macro_handler_test(dev, is_down, shift, ctrl):
    if is_down:
        dev.send_text("\\ test\n")
    else:
        dev.send_text("/ test\n")

def macro_handler_suspend_shutdown(dev, is_down, shift, ctrl):
    if not is_down:
        return
    if shift:
        print("Shutting Down...")
        dev.backlight.off()
        dev.backlight.on(r=0xFF, g=0x00, b=0x00)
        sleep(1.0)
        dev.backlight.off()

        microcontroller.reset()
    else:
        print("Suspending...")
        dev.suspend()
    
def macro_handler_plt(dev, is_down, shift, ctrl):
    if not is_down:
        return
    dev.send_text("import matplotlib.pyplot as plt\n")
    dev.send_text("plt.imshow(); plt.show()")
    for _ in range(13):
        dev.send(LEFT)

def macro_handler(dev, n, is_down, shift, ctrl):
    """
    Parameters
    ----------
    dev : Keyboard Device
        Useful methods:
            ``dev.send(GUI, R)``
            ``dev.send_text('calc\n')``
            ``dev.backlight.pixel(i, r, g, b)``
            ``dev.backlight.set_brightness(val)  # sets the global brightness of all LEDs``
            ``dev.backlight.update()  # push changes``
    n : int
        Macro identifier pressed
    is_down : bool
        If ``True``, then the button is pressed. If ``False``, the button is released.
    """

    macro_lookup = {
                MACRO_BATT: macro_handler_batt,
                MACRO_REPL: macro_handler_repl,
                MACRO_INSTALL_VIM: macro_handler_install_vim,
                MACRO_INSTALL_TMUX: macro_handler_install_tmux,
                MACRO_ZPROFILE: macro_handler_zprofile,
                MACRO_RGB_VAL_DEC: macro_handler_rgb_val_dec,
                MACRO_RGB_VAL_INC: macro_handler_rgb_val_inc,
                MACRO_IPDB: macro_handler_ipdb,
                MACRO_TEST: macro_handler_test,
                MACRO_SUSPEND_SHUTDOWN: macro_handler_suspend_shutdown,
                MACRO_PLT: macro_handler_plt,
            }

    handler = macro_lookup.get(n)
    if handler is not None:
        handler(dev, is_down, shift, ctrl)


# ESC(0)    1(1)   2(2)   3(3)   4(4)   5(5)   6(6)   7(7)   8(8)   9(9)   0(10)  -(11)  =(12)  BACKSPACE(13)
# TAB(27)   Q(26)  W(25)  E(24)  R(23)  T(22)  Y(21)  U(20)  I(19)  O(18)  P(17)  [(16)  ](15)   \(14)
# CAPS(28)  A(29)  S(30)  D(31)  F(32)  G(33)  H(34)  J(35)  K(36)  L(37)  ;(38)  "(39)      ENTER(40)
#LSHIFT(52) Z(51)  X(50)  C(49)  V(48)  B(47)  N(46)  M(45)  ,(44)  .(43)  /(42)            RSHIFT(41)
# LCTRL(53)  LGUI(54)  LALT(55)               SPACE(56)          RALT(57)  MENU(58)  Fn(59)  RCTRL(60)

#No.61 and No.62 are under the space key. No.63 is at the back of keyboard.

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))


keyboard.macro_handler = macro_handler
keyboard.pairs_handler = pairs_handler

#keyboard.matrix.debounce_time = 6
#keyboard.tap_delay = 200
#keyboard.fast_type_thresh = 100

# Pairs: J & K, U & I
#keyboard.pairs = [{35, 36}, {20, 19}]

keyboard.verbose = False

# Set backlight to monochrome amber
keyboard.backlight.hue = 7
keyboard.backlight.sat = 255
keyboard.backlight.val = 100
keyboard.backlight.set_mode(1)  # Mono mode

keyboard.run()
