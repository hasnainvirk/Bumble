"""
This module is used to test the remote control functionality. It listens to the remote control
"""

import logging
from components.remote_control.modules.cli_infrared_recvr import (
    CliInfrared as infra_red_recvr,
)
from components.remote_control.modules.buttons import (
    ButtonControls as button_controls,
    button_key_codes,
)
from components.remote_control.modules.buttons import (
    ButtonActionConfig as button_action_config,
)


class RemoteControlTest:
    """
    Class to test the remote control module
    """

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
        """
        Executes the command to listen to the remote control
        """
        for item in button_key_codes.items():
            self.action_config = {
                "key": item[1],
                "action": self.callables[item[0]],
            }
            self.button_controls[item[0]] = self.action_config

        self.ir.listen_and_process(self.button_controls)

    def up(self):
        """
        Function to be executed when the up button is pressed
        """
        self.log.info("up")

    def left(self):
        """
        Function to be executed when the left button is pressed
        """
        self.log.info("left")

    def ok(self):
        """
        Function to be executed when the ok button is pressed
        """
        self.log.info("ok")

    def right(self):
        """
        Function to be executed when the right button is pressed
        """
        self.log.info("right")

    def down(self):
        """
        Function to be executed when the down button is pressed
        """
        self.log.info("down")

    def one(self):
        """
        Function to be executed when the one button is pressed
        """
        self.log.info("one")

    def two(self):
        """
        Function to be executed when the two button is pressed
        """
        self.log.info("two")

    def three(self):
        """
        Function to be executed when the three button is pressed
        """
        self.log.info("three")

    def four(self):
        """
        Function to be executed when the four button is pressed
        """
        self.log.info("four")

    def five(self):
        """
        Function to be executed when the five button is pressed
        """
        self.log.info("five")

    def six(self):
        """
        Function to be executed when the six button is pressed
        """
        self.log.info("six")

    def seven(self):
        """
        Function to be executed when the seven button is pressed
        """
        self.log.info("seven")

    def eight(self):
        """
        Function to be executed when the eight button is pressed
        """
        self.log.info("eight")

    def nine(self):
        """
        Function to be executed when the nine button is pressed
        """
        self.log.info("nine")

    def asterisk(self):
        """
        Function to be executed when the asterisk button is pressed
        """
        self.log.info("asterisk")

    def zero(self):
        """
        Function to be executed when the zero button is pressed
        """
        self.log.info("zero")

    def hash(self):
        """
        Function to be executed when the hash button is pressed
        """
        self.log.info("hash")
