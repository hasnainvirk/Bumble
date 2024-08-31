"""
This module is responsible for handling the remote control commands.
"""

import logging
import threading
import queue
from components.remote_control.modules.infrared_recvr_task import (
    InfraredReceiver as infra_red_recvr,
)
from components.remote_control.modules.buttons import (
    ButtonControls as button_controls,
    button_key_codes,
)
from components.remote_control.modules.buttons import (
    ButtonActionConfig as button_action_config,
)

from components.drive_system.modules.drive_system import DriveSystem as drive_system


class RemoteControlHelper:
    """
    Class to handle the remote control commands
    """

    def __init__(self):
        self.__button_controls = button_controls()
        self.__action_config = button_action_config()
        self.__log = logging.getLogger("bumble")
        self.__queue = queue.Queue()
        self.__callables = {
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

        for item in button_key_codes.items():
            self.__action_config = {
                "key": item[1],
                "action": self.__callables[item[0]],
            }
            self.__button_controls[item[0]] = self.__action_config

        self.__ir = infra_red_recvr(self.__button_controls)
        self.__drive_system = drive_system(speed=30)
        self.__thread = threading.Thread(
            target=self.__worker, name="IR Helper Worker", daemon=False
        )

    def start(self):
        """
        Start the remote control module
        shutdown must be called to stop the module
        """
        self.__drive_system.start()
        self.__ir.start()
        self.__thread.start()

    def shutdown(self):
        """
        Shutdown the remote control module
        """
        self.__queue.put(None)
        self.__drive_system.shutdown()
        self.__ir.shutdown()
        self.__thread.join()

    def __worker(self):
        while True:
            message = self.__queue.get()
            if message is None:
                break

            self.__log.info("Processing message: %s", message)

            if message == "UP":
                self.__drive_system.post_message(
                    "forward", slow_down=False, delay=0.1, step=0.1
                )
            elif message == "DOWN":
                self.__drive_system.post_message(
                    "backward", slow_down=False, delay=0.1, step=0.1
                )
            elif message == "LEFT":
                self.__drive_system.post_message(
                    "left", slow_down=False, delay=0.1, step=5
                )
            elif message == "RIGHT":
                self.__drive_system.post_message(
                    "right", slow_down=False, delay=0.1, step=5
                )
            elif message == "STOP":
                self.__drive_system.post_message(
                    "none", slow_down=True, delay=0.1, step=5
                )
            else:
                self.__log.error("Invalid command: %s", message)
                self.__drive_system.post_message(
                    "none", slow_down=True, delay=0.1, step=5
                )

            self.__queue.task_done()

    def up(self):
        """
        Function to be executed when the up button is pressed
        """
        self.__log.info("up")
        self.__queue.put("UP")

    def left(self):
        """
        Function to be executed when the left button is pressed
        """
        self.__log.info("left")
        self.__queue.put("LEFT")

    def ok(self):
        """
        Function to be executed when the ok button is pressed
        """
        self.__log.info("ok")

    def right(self):
        """
        Function to be executed when the right button is pressed
        """
        self.__log.info("right")
        self.__queue.put("RIGHT")

    def down(self):
        """
        Function to be executed when the down button is pressed
        """
        self.__log.info("down")
        self.__queue.put("DOWN")

    def one(self):
        """
        Function to be executed when the one button is pressed
        """
        self.__log.info("one")

    def two(self):
        """
        Function to be executed when the two button is pressed
        """
        self.__log.info("two")

    def three(self):
        """
        Function to be executed when the three button is pressed
        """
        self.__log.info("three")

    def four(self):
        """
        Function to be executed when the four button is pressed
        """
        self.__log.info("four")

    def five(self):
        """
        Function to be executed when the five button is pressed
        """
        self.__log.info("five")

    def six(self):
        """
        Function to be executed when the six button is pressed
        """
        self.__log.info("six")

    def seven(self):
        """
        Function to be executed when the seven button is pressed
        """
        self.__log.info("seven")

    def eight(self):
        """
        Function to be executed when the eight button is pressed
        """
        self.__log.info("eight")

    def nine(self):
        """
        Function to be executed when the nine button is pressed
        """
        self.__log.info("nine")

    def asterisk(self):
        """
        Function to be executed when the asterisk button is pressed
        """
        self.__log.info("asterisk")
        self.__queue.put("STOP")

    def zero(self):
        """
        Function to be executed when the zero button is pressed
        """
        self.__log.info("zero")

    def hash(self):
        """
        Function to be executed when the hash button is pressed
        """
        self.__log.info("hash")
