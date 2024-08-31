"""
This module contains the configuration for the buttons on the remote control.
"""

from typing import TypedDict


button_key_codes = {
    "up": 0x46,
    "left": 0x44,
    "ok": 0x40,
    "right": 0x43,
    "down": 0x15,
    "one": 0x16,
    "two": 0x19,
    "three": 0x0D,
    "four": 0x0C,
    "five": 0x18,
    "six": 0x5E,
    "seven": 0x08,
    "eight": 0x1C,
    "nine": 0x5A,
    "asterisk": 0x42,
    "zero": 0x52,
    "hash": 0x4A,
}


class ButtonActionConfig(TypedDict):
    """Configuration for a button action"""

    key: int
    action: callable


class ButtonControls(TypedDict):
    """Configuration for the buttons on the remote control"""

    up: ButtonActionConfig
    left: ButtonActionConfig
    ok: ButtonActionConfig
    right: ButtonActionConfig
    down: ButtonActionConfig
    one: ButtonActionConfig
    two: ButtonActionConfig
    three: ButtonActionConfig
    four: ButtonActionConfig
    five: ButtonActionConfig
    six: ButtonActionConfig
    seven: ButtonActionConfig
    eight: ButtonActionConfig
    nine: ButtonActionConfig
    asterisk: ButtonActionConfig
    zero: ButtonActionConfig
    hash: ButtonActionConfig
