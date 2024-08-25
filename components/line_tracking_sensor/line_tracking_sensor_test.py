from components.line_tracking_sensor.modules.line_tracking_sensor import (
    LineTrackingSensor,
    line_ctrl,
)
import logging, time


class LineTrackingSensorTest:
    def __init__(self) -> None:
        self.__line_tracking_sensor = LineTrackingSensor()
        self.log = logging.getLogger("bumble")

    def execute_command(self) -> None:
        try:
            while True:
                time.sleep(1)
                retval: line_ctrl = self.__line_tracking_sensor.read()
                self.log.info(f"Decision: {retval.get('decision')}")
        except KeyboardInterrupt:
            self.__line_tracking_sensor.cleanup()
            self.log.info("Exiting Line Tracking Sensor Test")
