import RPi.GPIO as GPIO
from components.remote_control.modules.buttons import (
    ButtonControls as button_ctrls,
    button_key_codes,
)
from components.remote_control.modules.infrared_recvr_base import InfraredRecvrBase
import logging, time


GPIO_15 = 15
SIXTY_MICROSECONDS_IN_SECONDS = 0.00006  # apptoximately


class CliInfrared(InfraredRecvrBase):
    def __init__(self):
        self.log = logging.getLogger("bumble")
        self.pin = GPIO_15
        super().__init__(self.pin)

    def listen_and_process(self, button_ctrls: button_ctrls):
        try:
            while True:
                if GPIO.input(self.pin) == 0:
                    # self.recv_preamble()
                    self.recv_data()
                    if self.verify_data():
                        data = self.data[2]
                        self.log.debug(f"Received data: {data}")
                        for command in button_key_codes:
                            if button_key_codes[command] == data:
                                self.log.debug(f"calling button controller: {command}")
                                button_ctrls[command][
                                    "action"
                                ]()  # calls the callable object
                                break
        except KeyboardInterrupt:
            self.cleanup()
