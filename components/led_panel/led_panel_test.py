from components.led_panel.modules.shapes import (
    bob_eyes_shut,
    bob_eyes_open,
    smile,
    matrix_forward,
    matrix_back,
    matrix_left,
    matrix_right,
)
from typing import TypedDict, Optional
from components.led_panel.modules.led_panel import LedPanel
import time, logging

led_cmd_options = TypedDict(
    "led_cmd_options",
    {
        "smile": Optional[bool],
        "bob": Optional[bool],
    },
)


class LedPanelTest(object):
    def __init__(self):
        self.__bob_eyes_open = bob_eyes_open
        self.__bob_eyes_shut = bob_eyes_shut
        self.__smile = smile
        self.__matrix_forward = matrix_forward
        self.__matrix_back = matrix_back
        self.__matrix_left = matrix_left
        self.__matrix_right = matrix_right
        self.__panel = LedPanel()
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts: led_cmd_options):
        try:
            while True:
                if cmd_opts.get("smile"):
                    self.__panel.display(self.__smile)
                    time.sleep(1)
                    self.__panel.display(self.__matrix_back)
                    time.sleep(1)
                    self.__panel.display(self.__matrix_forward)
                    time.sleep(1)
                    self.__panel.display(self.__matrix_left)
                    time.sleep(1)
                    self.__panel.display(self.__matrix_right)
                elif cmd_opts.get("bob"):
                    self.__panel.display(self.__bob_eyes_open)
                    time.sleep(1)
                    self.__panel.display(self.__bob_eyes_shut)
                    time.sleep(1)
        except KeyboardInterrupt:
            self.__panel.clear()
            self.__panel.cleanup()
            self.log.info("Exiting Led Panel Test")
