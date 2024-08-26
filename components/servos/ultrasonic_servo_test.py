from components.servos.modules.ultrasonic_sensor_servo import (
    UltrasonicSensorServo as ultrasonic_sensor_servo,
)
import logging
from typing import TypedDict, Optional


servo_cmd_options = TypedDict(
    "servo_cmd_options",
    {
        "point": Optional[str],
        "rotate": Optional[str],
        "tilt": Optional[str],
    },
)


class UltrasonicSensorServoTest:
    def __init__(self):
        self.servo = ultrasonic_sensor_servo()
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts: servo_cmd_options):
        if cmd_opts.get("point"):
            self.__handle_point(cmd_opts["point"])
        elif cmd_opts.get("rotate"):
            self.__handle_rotate(cmd_opts["rotate"])
        else:
            raise ValueError("Invalid command options")

    def __handle_point(self, point: str):
        if point == "straight":
            self.servo.point_straight()
        elif point == "right":
            self.servo.point_right()
        elif point == "left":
            self.servo.point_left()
        else:
            raise ValueError("Invalid point direction")

    def __handle_rotate(self, rotate: str):
        if rotate == "center":
            self.servo.rotate_center()
        elif rotate == "right":
            self.servo.rotate_right()
        elif rotate == "left":
            self.servo.rotate_left()
        else:
            raise ValueError("Invalid rotate direction")
