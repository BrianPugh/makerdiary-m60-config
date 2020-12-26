#from PYKB import *
from keyboard import *

MACRO_BATT = 1

keyboard = Keyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')

keyboard.keymap = (
    # layer 0
    (
        ESC,    1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,    Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        L1,     A,   S,   D,   F,   G,   H,   J,   K,   L, ';', '"',    ENTER,
        LSHIFT, Z,   X,   C,   V,   B,   N,   M, ',', '.', '/',         RSHIFT,
        LCTRL, LGUI, LALT,          SPACE,            RALT,  MENU,  L1,   RCTRL
    ),

    # layer 1
    (
        '`',  F1,      F2,      F3,   F4,   F5,   F6,   F7,    F8,    F9,    F10,  F11, F12, DEL,
        ___, ___,     ___,     ___, BOOT,  ___,  ___, PGUP,    UP,  PGDN, PRTSCN,  ___, ___, ___,
        ___, ___,   VOLDN,   VOLUP, MUTE, ___, HOME, LEFT,  DOWN, RIGHT, INSERT,  ___,      ___,
        ___, ___, BRGHTDN, BRGHTUP, ___,  MACRO(MACRO_BATT),  END,  ___,   ___,   ___,    ___, ___,
        ___, ___,   ___,                   ___,                     ___,   ___,   ___,      ___
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


def macro_handler(dev, n, is_down):
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

    if n == MACRO_BATT:
        if is_down:
            dev.send_text('You pressed macro #{}\n'.format(n))
        else:
            dev.send_text('You pressed macro #{}\n'.format(n))
    #if is_down:
    #    dev.send_text('You pressed macro #{}\n'.format(n))
    #else:
    #    dev.send_text('You released macro #{}\n'.format(n))


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

# Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]

keyboard.verbose = False

#keyboard.backlight.pixel(56, 0xFF, 0x1F, 0x00)
#for i in range(61):
#    keyboard.backlight.pixel(i, 0xFF, 0x1F, 0x00)
##keyboard.backlight.set_brightness(30)
#keyboard.backlight.set_brightness(200)
#keyboard.backlight.update()

keyboard.run()
