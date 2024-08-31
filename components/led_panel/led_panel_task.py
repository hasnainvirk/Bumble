"""
Led Panel Task
"""

import time
import logging
import threading

from components.led_panel.modules.shapes import (
    bob_eyes_shut,
    bob_eyes_open,
    bob_eyes_dead,
)

from components.led_panel.modules.led_panel import LedPanel


class LedPanelTask:
    """
    Led Panel Task class
    """

    def __init__(self):
        self.__bob_eyes_open = bob_eyes_open
        self.__bob_eyes_shut = bob_eyes_shut
        self.__bob_eyes_dead = bob_eyes_dead
        self.__panel = LedPanel()
        self.stop_flag = threading.Event()
        self.log = logging.getLogger("bumble")
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        """
        Starts the LED panel task.
        shutdown() must be called to stop the task.
        """
        self.thread = threading.Thread(target=self.display, name="Led Panel")
        self.thread.start()

    def shutdown(self):
        """
        Stops the LED panel task.
        """
        self.stop_flag.set()
        self.thread.join()

    def display(self):
        """
        Displays the eyes on the LED panel.
        """
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
