from components.led_panel.modules.shapes import (
    bob_face,
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
        self.__bob_face = bob_face
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
                self.__panel.display(self.__smile)
                time.sleep(1)
                self.__panel.display(self.__matrix_back)
                time.sleep(1)
                self.__panel.display(self.__matrix_forward)
                time.sleep(1)
                self.__panel.display(self.__matrix_left)
                time.sleep(1)
                self.__panel.display(self.__matrix_right)
        except KeyboardInterrupt:
            self.__panel.clear()
            self.__panel.cleanup()
            self.log.info("Exiting Led Panel Test")
