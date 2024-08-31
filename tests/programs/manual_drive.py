"""
This is a manual drive program that allows the user to control the 
robot using a remote control or keyboard.
"""

import logging
import signal
import sys
from typing import Optional, TypedDict

import RPi.GPIO as GPIO

from components.led_panel.led_panel_task import LedPanelTask as led_panel
from components.oled.oled_task import OledDisplay as oled
from helpers.ir_helper import RemoteControlHelper as remote_control
from helpers.kb_controller_server import (
    KeyboardControllerServer as kb_controller_server,
)

GPIO.setwarnings(False)

manual_drive_cmd_options = TypedDict(
    "manual_drive_cmd_options",
    {
        "t": Optional[str],
    },
)


class ManualDrive:
    """
    Class to control the car manually using the remote control or keyboard
    """

    def __init__(self, mode: manual_drive_cmd_options) -> None:
        self.log = logging.getLogger("bumble")
        self.log.debug("Mode: %s", mode.get("t"))
        self.controller = None
        if mode.get("t") == "ir":
            self.log.info("Starting in IR mode")
            self.controller = remote_control()
        elif mode.get("t") == "kb":
            self.log.info("Starting in KEYBOARD mode")
            self.controller = kb_controller_server()

        self.oled = oled()
        self.led_panel = led_panel()

        # Register the signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, __signum, __frame):
        """
        Signal handler to handle the exit signal
        """
        self.log.info("Exit signal received. Exiting...")
        if self.controller:
            self.controller.shutdown()
        self.oled.shutdown()
        self.led_panel.shutdown()

        sys.exit(0)

    def start(self):
        """
        Start the manual drive program
        """
        # START INPUT CONTROLLER
        if self.controller:
            self.controller.start()
        # START OLED
        self.oled.start()
        # START LED PANEL
        self.led_panel.start()

        # wait for exit signal
        signal.pause()
