"""
Online Resources
----------------
https://wiki.makerdiary.com/m60/

General Notes
-------------
* When connecting the keyboard to a computer via USB, USB will be enabled 
  automatically. When both USB and Bluetooth are enabled, USB will be used.

Special Keycodes
----------------
NO              Do nothing
TRANSPARENT     Use the key of next active layer

BT0 ~ BT9       Switch to Bluetooth ID n (0 - 9)
BT_TOGGLE       Toggle Bluetooth
USB_TOGGLE      Toggle USB

BOOTLOADER      Enter the bootloader of the keyboard
SUSPEND         Suspend. To wake up keyboard, just press any key
SHUTDOWN        Shutdown. Use ON/OFF button to power on the keyboard

Layer & Modifier
----------------

`MODS_KEY(mods, key)` sends one or more modifier(s) + a normal key. `MODS()` is used to wrap modifiers.
`MODS_KEY(MODS(LCTRL), C)`, `MODS_KEY(MODS(LCTRL, LSHIFT), C)`, `MODS_KEY(MODS(LCTRL, LSHIFT, LALT), C)`
* `LAYER_TOGGLE(n)` toggles layer `n`
* `MACRO(n)` creates macro `n`

TAP-Key
^^^^^^^
A `TAP-Key` has 2 modes - tap (press and release quickly) and hold (long press)

* `LAYER_TAP(n, key)` tap - outputs `key`, hold - turns on layer n momentary
* `LAYER_TAP_TOGGLE(n)` tap - toggles layer n, hold - turns on layer n momentary
* `LAYER_MODS(n, mods)` tap - outputs specified modifier(s), hold - turns on 
  layer n momentary `LAYER_MODS(1, MODS(LCTRL))`, `LAYER_MODS(1, MODS(LCTRL, LSHIFT))`
* `MODS_TAP(mods, key)` tap - outputs `key`, hold - outputs specified modifier(s)
  `MODS_TAP(MODS(LCTRL), ';')`, `MODS_TAP(MODS(LCTRL, LALT), LEFT)`

App and Media
-------------
.. code-block::
    AUDIO_MUTE
    AUDIO_VOL_UP
    AUDIO_VOL_DOWN
    TRANSPORT_NEXT_TRACK
    TRANSPORT_PREV_TRACK
    TRANSPORT_STOP
    TRANSPORT_STOP_EJECT
    TRANSPORT_PLAY_PAUSE
    # application launch
    APPLAUNCH_CC_CONFIG
    APPLAUNCH_EMAIL
    APPLAUNCH_CALCULATOR
    APPLAUNCH_LOCAL_BROWSER
    # application control
    APPCONTROL_SEARCH
    APPCONTROL_HOME
    APPCONTROL_BACK
    APPCONTROL_FORWARD
    APPCONTROL_STOP
    APPCONTROL_REFRESH
    APPCONTROL_BOOKMARKS
    # supplement for Bluegiga iWRAP HID(not supported by Windows?)
    APPLAUNCH_LOCK
    TRANSPORT_RECORD
    TRANSPORT_FAST_FORWARD
    TRANSPORT_REWIND
    TRANSPORT_EJECT
    APPCONTROL_MINIMIZE
    # https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/display-brightness-control
    DISPLAY_BRIGHTNESS_UP
    DISPLAY_BRIGHTNESS_DOWN

Normal Keys
-----------
.. code-block::
    A
    B
    C
    D
    E
    F
    G
    H
    I
    J
    K
    L
    M
    N
    O
    P
    Q
    R
    S
    T
    U
    V
    W
    X
    Y
    Z

    1
    2
    3
    4
    5
    6
    7
    8
    9
    0

    ENTER
    ESCAPE
    ESC
    BACKSPACE
    TAB
    SPACE
    MINUS
    EQUAL
    LEFTBRACE
    RIGHTBRACE
    BACKSLASH
    HASHTILDE
    SEMICOLON
    APOSTROPHE
    QUOTE
    GRAVE
    COMMA
    DOT
    SLASH
    CAPSLOCK
    CAPS

    F1
    F2
    F3
    F4
    F5
    F6
    F7
    F8
    F9
    F10
    F11
    F12

    PRINTSCREEN
    PRTSCN
    SCROLLLOCK
    PAUSE
    INSERT
    HOME
    PAGEUP
    PGUP
    DELETE
    DEL
    END
    PAGEDOWN
    PGDN
    RIGHT
    LEFT
    DOWN
    UP

    NUMLOCK
    KPSLASH
    KPASTERISK
    KPMINUS
    KPPLUS
    KPENTER
    KP1
    KP2
    KP3
    KP4
    KP5
    KP6
    KP7
    KP8
    KP9
    KP0
    KPDOT

    APPLICATION
    MENU
    POWER
    KPEQUAL

    F13
    F14
    F15
    F16
    F17
    F18
    F19
    F20
    F21
    F22
    F23
    F24

    OPEN
    HELP
    SELECT
    STOP
    AGAIN
    UNDO
    CUT
    COPY
    PASTE
    FIND
    MUTE
    KPCOMMA

    INT1
    INT2
    INT3
    INT4
    INT5
    INT6
    INT7
    INT8
    INT9

    RO
    KATAKANAHIRAGANA
    YEN
    HENKAN
    MUHENKAN
    KPJPCOMMA

    LANG1
    LANG2
    LANG3
    LANG4
    LANG5
    LANG6
    LANG7
    LANG8
    LANG9

    HANGEUL
    HANJA
    KATAKANA
    HIRAGANA
    ZENKAKUHANKAKU

    KPLEFTPAREN
    KPRIGHTPAREN

    LEFT_CTRL
    LEFT_SHIFT
    LEFT_ALT
    LEFT_GUI
    RIGHT_CTRL
    RIGHT_SHIFT
    RIGHT_ALT
    RIGHT_GUI

    LCTRL
    LSHIFT
    LALT
    LGUI
    RCTRL
    RSHIFT
    RALT
    RGUI

    CTRL
    SHIFT
    ALT
    GUI
"""

from PYKB import *

keyboard = Keyboard()

___ = TRANSPARENT
BOOT = BOOTLOADER
L1 = LAYER_TAP(1)
L2D = LAYER_TAP(2, D)
L3B = LAYER_TAP(3, B)
LSFT4 = LAYER_MODS(4, MODS(LSHIFT))
RSFT4 = LAYER_MODS(4, MODS(RSHIFT))

# Semicolon & Ctrl
SCC = MODS_TAP(MODS(RCTRL), ';')

keyboard.keymap = (
    # layer 0
    (
        ESC,   1,   2,   3,   4,   5,   6,   7,   8,   9,   0, '-', '=', BACKSPACE,
        TAB,   Q,   W,   E,   R,   T,   Y,   U,   I,   O,   P, '[', ']', '|',
        CAPS,  A,   S, L2D,   F,   G,   H,   J,   K,   L, SCC, '"',    ENTER,
        LSFT4, Z,   X,   C,   V, L3B,   N,   M, ',', '.', '/',         RSFT4,
        LCTRL, LGUI, LALT,          SPACE,            RALT, MENU,  L1, RCTRL
    ),

    # layer 1
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___,  UP, ___, ___, ___, ___, ___, ___, ___,SUSPEND,___,___,___,
        ___,LEFT,DOWN,RIGHT,___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___,BOOT, ___,MACRO(0), ___, ___, ___,       ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 2
    (
        '`',  F1,  F2,  F3,  F4,  F5,  F6,  F7,  F8,  F9, F10, F11, F12, DEL,
        ___, ___, ___, ___, ___, ___, ___,PGUP, ___, ___, ___,AUDIO_VOL_DOWN,AUDIO_VOL_UP,AUDIO_MUTE,
        ___, ___, ___, ___, ___, ___,LEFT,DOWN, UP,RIGHT, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___,PGDN, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 3
    (
        BT_TOGGLE,BT1,BT2, BT3,BT4,BT5,BT6,BT7, BT8, BT9, BT0, ___, ___, ___,
        ___, ___, ___, ___, ___, ___,___,USB_TOGGLE,___,___,___,___,___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,      ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),

    # layer 4
    (
        '`', ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___, ___,
        ___, ___, ___,   D, ___, ___, ___, ___, ___, ___, ';', ___,      ___,
        ___, ___, ___, ___, ___,   B, ___, ___, ___, ___, ___,           ___,
        ___, ___, ___,                ___,               ___, ___, ___,  ___
    ),
)


def macro_handler(dev, n, is_down):
    if is_down:
        dev.send_text('You pressed macro #{}\n'.format(n))
    else:
        dev.send_text('You released macro #{}\n'.format(n))

def pairs_handler(dev, n):
    dev.send_text('You just triggered pair keys #{}\n'.format(n))


keyboard.macro_handler = macro_handler
keyboard.pairs_handler = pairs_handler

# Pairs: J & K, U & I
keyboard.pairs = [{35, 36}, {20, 19}]

keyboard.verbose = False

keyboard.run()
