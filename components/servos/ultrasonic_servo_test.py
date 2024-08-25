from components.servos.modules.ultrasonic_sensor_servo import (
    UltrasonicSensorServo as ultrasonic_sensor_servo,
)
import logging
from typing import TypedDict, Optional


servo_cmd_options = TypedDict(
    "servo_cmd_options",
    {
        "straight": Optional[bool],
        "right": Optional[bool],
        "left": Optional[bool],
    },
)


class UltrasonicSensorServoTest:
    def __init__(self):
        self.servo = ultrasonic_sensor_servo()
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts: servo_cmd_options):
        if cmd_opts.get("straight"):
            self.servo.point_straight()
        elif cmd_opts.get("right"):
            self.servo.turn_right()
        elif cmd_opts.get("left"):
            self.servo.turn_left()
        else:
            raise ValueError("Invalid command options")
