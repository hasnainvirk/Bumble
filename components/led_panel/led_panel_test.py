"""
Led Panel Test
"""

from typing import TypedDict, Optional
import time
import logging
from components.led_panel.modules.shapes import (
    bob_eyes_shut,
    bob_eyes_open,
    smile,
    matrix_forward,
    matrix_back,
    matrix_left,
    matrix_right,
)
from components.led_panel.modules.led_panel import LedPanel


led_cmd_options = TypedDict(
    "led_cmd_options",
    {
        "smile": Optional[bool],
        "bob": Optional[bool],
    },
)


class LedPanelTest(object):
    """
    Led Panel Test class
    """

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
        """
        Executes the command based on the given options

        Args: cmd_opts (led_cmd_options): A dictionary containing the command options.
            - smile (Optional[bool]): Displays smiley face on the LED panel.
            - bob (Optional[bool]): Displays bob face on the LED panel.

            raise KeyboardInterrupt: If the user interrupts the program.
        """
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
