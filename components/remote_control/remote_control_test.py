from components.remote_control.modules.infrared_recvr import (
    InfraRedRecvr as infra_red_recvr,
)
from components.remote_control.modules.buttons import (
    ButtonControls as button_controls,
    button_key_codes,
)
from components.remote_control.modules.buttons import (
    ButtonActionConfig as button_action_config,
)

import logging


class RemoteControlTest:
    def __init__(self):
        self.ir = infra_red_recvr()
        self.button_controls = button_controls()
        self.action_config = button_action_config()
        self.log = logging.getLogger("bumble")
        self.callables = {
            "up": self.up,
            "left": self.left,
            "ok": self.ok,
            "right": self.right,
            "down": self.down,
            "one": self.one,
            "two": self.two,
            "three": self.three,
            "four": self.four,
            "five": self.five,
            "six": self.six,
            "seven": self.seven,
            "eight": self.eight,
            "nine": self.nine,
            "asterisk": self.asterisk,
            "zero": self.zero,
            "hash": self.hash,
        }

    def execute_command(self):
        for key in button_key_codes:
            self.action_config[key] = {
                "key": button_key_codes[key],
                "action": self.callables[key],
            }
            self.button_controls[key] = self.action_config[key]

        self.ir.listen_and_process(self.button_controls)

    def up(self):
        self.log.info("up")

    def left(self):
        self.log.info("left")

    def ok(self):
        self.log.info("ok")

    def right(self):
        self.log.info("right")

    def down(self):
        self.log.info("down")

    def one(self):
        self.log.info("one")

    def two(self):
        self.log.info("two")

    def three(self):
        self.log.info("three")

    def four(self):
        self.log.info("four")

    def five(self):
        self.log.info("five")

    def six(self):
        self.log.info("six")

    def seven(self):
        self.log.info("seven")

    def eight(self):
        self.log.info("eight")

    def nine(self):
        self.log.info("nine")

    def asterisk(self):
        self.log.info("asterisk")

    def zero(self):
        self.log.info("zero")

    def hash(self):
        self.log.info("hash")
