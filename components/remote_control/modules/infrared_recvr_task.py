"""
This module is responsible for receiving infrared signals from the remote control.
"""

import logging
import threading
import RPi.GPIO as GPIO
from components.remote_control.modules.buttons import (
    ButtonControls as button_ctrls,
    button_key_codes,
)
from components.remote_control.modules.infrared_recvr_base import (
    InfraredRecvrBase as Base,
)


GPIO_15 = 15
SIXTY_MICROSECONDS_IN_SECONDS = 0.00006  # apptoximately


class InfraredReceiver(Base):
    """
    Infrared Receiver class
    """

    def __init__(self, ctrls: button_ctrls):
        self.log = logging.getLogger("bumble")
        self.pin = GPIO_15
        self.ctrls = ctrls
        self.lock = threading.Lock()
        self.thread = None
        super().__init__(self.pin)

    def start(self):
        """
        Starts the infrared receiver
        shutdown() must be called to stop the receiver.
        """
        # Start the infrared receiver in a separate thread
        self.thread = threading.Thread(
            target=self.__worker,
            name="IR Receiver",
        )
        self.thread.daemon = False
        self.thread.start()

    def shutdown(self):
        """
        Stops the infrared receiver
        """
        # remove the interrupt
        GPIO.remove_event_detect(self.pin)
        self.thread.join()
        GPIO.cleanup(self.pin)

    def __worker(self):
        # Set up an interrupt to detect the signal
        try:
            GPIO.add_event_detect(
                self.pin, GPIO.FALLING, callback=self.__handle_interrupt
            )
        except RuntimeError as e:
            self.log.critical("Failed to add edge detection: %s", e)
            self.cleanup()

    def __handle_interrupt(self, channel):
        with self.lock:
            if GPIO.input(channel) == 0:
                # self.recv_preamble()
                self.recv_data()
                if self.verify_data():
                    data = self.data[2]
                    for command in button_key_codes.items():
                        if command[1] == data:
                            self.ctrls[command[0]]["action"]()
                            break
