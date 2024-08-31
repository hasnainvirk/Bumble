"""
Line Tracking Sensor Test
"""

import logging
import time
from components.line_tracking_sensor.modules.line_tracking_sensor import (
    LineTrackingSensor,
    line_ctrl,
)


class LineTrackingSensorTest:
    """
    Line Tracking Sensor Test class
    """

    def __init__(self) -> None:
        self.__line_tracking_sensor = LineTrackingSensor()
        self.log = logging.getLogger("bumble")

    def execute_command(self) -> None:
        """
        Executes the command to read the line tracking sensor
        """
        try:
            while True:
                time.sleep(1)
                retval: line_ctrl = self.__line_tracking_sensor.read()
                self.log.info("Decision: %s", retval["decision"])
        except KeyboardInterrupt:
            self.__line_tracking_sensor.cleanup()
            self.log.info("Exiting Line Tracking Sensor Test")
