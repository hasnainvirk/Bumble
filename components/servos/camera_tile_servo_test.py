from components.servos.modules.camera_tilt_servo import (
    CameraTiltServo as camera_tilt_servo,
)
import logging
from typing import TypedDict, Optional


# servo_cmd_options = TypedDict(
#     "servo_cmd_options",
#     {
#         "point": Optional[str],
#         "rotate": Optional[str],
#     },
# )


class CameraTiltServoTest:
    def __init__(self):
        self.servo = camera_tilt_servo()
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts):
        if cmd_opts.get("tilt"):
            self.__handle_tilt(cmd_opts["tilt"])
        else:
            raise ValueError("Invalid command options")

    def __handle_tilt(self, point: str):
        if point == "center":
            self.servo.tilt_center()
        elif point == "down":
            self.servo.tilt_down()
        elif point == "up":
            self.servo.tilt_up()
        else:
            raise ValueError("Invalid point direction")
