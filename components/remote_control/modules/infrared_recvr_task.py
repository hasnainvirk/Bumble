import RPi.GPIO as GPIO
from components.remote_control.modules.buttons import (
    ButtonControls as button_ctrls,
    button_key_codes,
)
from components.remote_control.modules.infrared_recvr_base import (
    InfraredRecvrBase as Base,
)
import logging, time, threading


GPIO_15 = 15
SIXTY_MICROSECONDS_IN_SECONDS = 0.00006  # apptoximately


class InfraredReceiver(Base):

    def __init__(self, ctrls: button_ctrls):
        self.log = logging.getLogger("bumble")
        self.pin = GPIO_15
        self.data = [0, 0, 0, 0]
        self.ctrls = ctrls
        self.lock = threading.Lock()
        super().__init__(self.pin, self.data)

    def start(self):
        # Start the infrared receiver in a separate thread
        self.thread = threading.Thread(
            target=self.__worker,
            name="IR Receiver",
        )
        self.thread.daemon = False
        self.thread.start()

    def shutdown(self):
        # remove the interrupt
        GPIO.remove_event_detect(self.pin)
        # GPIO.cleanup(self.pin)
        self.thread.join()

    def __worker(self):
        # Set up an interrupt to detect the signal
        try:
            GPIO.add_event_detect(
                self.pin, GPIO.FALLING, callback=self.__handle_interrupt
            )
        except RuntimeError as e:
            self.log.error(f"Failed to add edge detection: {e}")
            GPIO.cleanup(self.pin)

    def __handle_interrupt(self, channel):
        with self.lock:
            if GPIO.input(channel) == 0:
                self.recv_preamble()
                self.recv_data()
                if self.verify_data():
                    data = self.data[2]
                    for command in button_key_codes:
                        if button_key_codes[command] == data:
                            self.ctrls[command]["action"]()  # calls the callable object
                            break
