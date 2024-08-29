from components.led_panel.modules.shapes import (
    bob_eyes_shut,
    bob_eyes_open,
    bob_eyes_dead,
)

from components.led_panel.modules.led_panel import LedPanel
import time, logging, threading


class LedPanelTask:
    def __init__(self):
        self.__bob_eyes_open = bob_eyes_open
        self.__bob_eyes_shut = bob_eyes_shut
        self.__bob_eyes_dead = bob_eyes_dead
        self.__panel = LedPanel()
        self.stop_flag = threading.Event()
        self.log = logging.getLogger("bumble")
        self.lock = threading.Lock()

    def start(self):
        self.thread = threading.Thread(target=self.display, name="Led Panel")
        self.thread.start()

    def shutdown(self):
        self.stop_flag.set()
        self.thread.join()

    def display(self):
        with self.lock:
            while True:
                if self.stop_flag.is_set():
                    break
                self.__panel.display(self.__bob_eyes_open)
                time.sleep(1)

                self.__panel.display(self.__bob_eyes_shut)
                time.sleep(1)

        self.__panel.display(self.__bob_eyes_dead)
        self.__panel.clear()
        self.__panel.cleanup()
