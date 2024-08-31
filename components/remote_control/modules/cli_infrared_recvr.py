"""
This module is responsible for receiving infrared signals from a remote control
"""

import logging
import RPi.GPIO as GPIO
from components.remote_control.modules.buttons import (
    ButtonControls as button_ctrls,
    button_key_codes,
)
from components.remote_control.modules.infrared_recvr_base import InfraredRecvrBase


GPIO_15 = 15
SIXTY_MICROSECONDS_IN_SECONDS = 0.00006  # apptoximately


class CliInfrared(InfraredRecvrBase):
    """
    CLI Infrared class
    """

    def __init__(self):
        self.log = logging.getLogger("bumble")
        self.pin = GPIO_15
        super().__init__(self.pin)

    def listen_and_process(self, ctrls: button_ctrls):
        """
        Listens for infrared signals and processes the received data
        """
        try:
            while True:
                if GPIO.input(self.pin) == 0:
                    # self.recv_preamble()
                    self.recv_data()
                    if self.verify_data():
                        data = self.data[2]
                        self.log.debug("Received data: %d", data)
                        for command in button_key_codes.items():
                            if data == command[1]:
                                self.log.debug(
                                    "calling button controller: %s", command[0]
                                )
                                ctrls[command[0]]["action"]()
                                break

        except KeyboardInterrupt:
            self.cleanup()
