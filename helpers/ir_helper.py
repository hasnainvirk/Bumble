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
import logging, threading, queue


class RemoteControlHelper:
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
        for key in button_key_codes:
            self.__action_config[key] = {
                "key": button_key_codes[key],
                "action": self.__callables[key],
            }
            self.__button_controls[key] = self.__action_config[key]

        self.__ir = infra_red_recvr(self.__button_controls)
        self.__drive_system = drive_system(speed=30)
        self.__thread = threading.Thread(
            target=self.__worker, name="IR Helper Worker", daemon=False
        )
        self.__stop_flag = threading.Event()

    def start(self):
        self.__drive_system.start()
        self.__ir.start()
        self.__thread.start()

    def shutdown(self):
        self.__queue.put(None)
        self.__drive_system.shutdown()
        self.__ir.shutdown()
        self.__thread.join()

    def __worker(self):
        while True:
            message = self.__queue.get()
            if message is None:
                break

            self.log.info(f"Processing message: {message}")

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
                self.__log.error(f"Invalid command: {message}")
                self.__drive_system.post_message(
                    "none", slow_down=True, delay=0.1, step=5
                )

            self.__queue.task_done()

    def up(self):
        self.__log.info("up")
        self.__queue.put("UP")

    def left(self):
        self.__log.info("left")
        self.__queue.put("LEFT")

    def ok(self):
        self.__log.info("ok")

    def right(self):
        self.__log.info("right")
        self.__queue.put("RIGHT")

    def down(self):
        self.__log.info("down")
        self.__queue.put("DOWN")

    def one(self):
        self.__log.info("one")

    def two(self):
        self.__log.info("two")

    def three(self):
        self.__log.info("three")

    def four(self):
        self.__log.info("four")

    def five(self):
        self.__log.info("five")

    def six(self):
        self.__log.info("six")

    def seven(self):
        self.__log.info("seven")

    def eight(self):
        self.__log.info("eight")

    def nine(self):
        self.__log.info("nine")

    def asterisk(self):
        self.__log.info("asterisk")
        self.__queue.put("STOP")

    def zero(self):
        self.__log.info("zero")

    def hash(self):
        self.__log.info("hash")
