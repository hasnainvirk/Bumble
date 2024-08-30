from components.servos.modules.ultrasonic_sensor_servo import (
    UltrasonicSensorServo as ultrasonic_sensor_servo,
)
from components.servos.modules.camera_servo import CameraServo as camera_servo
from components.servos.modules.servo_iface import SERVO_ID_TILT, SERVO_ID_ROTATION
import logging
from typing import TypedDict, Optional


servo_cmd_options = TypedDict(
    "servo_cmd_options",
    {
        "type": str,
        "servo_command": Optional[str],
        "tilt": Optional[str],
    },
)


class ServoTest:
    def __init__(self):
        self.servo = None
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts: servo_cmd_options):
        if cmd_opts["type"] == "ultrasonic":
            self.servo = ultrasonic_sensor_servo()
        elif cmd_opts["type"] == "camera":
            if cmd_opts.get("tilt") is not None:
                self.servo = camera_servo(tid=SERVO_ID_TILT)
            else:
                self.servo = camera_servo(tid=SERVO_ID_ROTATION)
        else:
            self.log.error("Invalid command options")
            return

        if self.servo is None:
            self.log.error("Servo not initialized")
            return

        if cmd_opts.get("servo_command") == "straight":
            self.servo.point_straight()
        elif cmd_opts.get("servo_command") == "right":
            self.servo.point_right()
        elif cmd_opts.get("servo_command") == "left":
            self.servo.point_left()

        if cmd_opts.get("tilt") == "open":
            self.servo.open_camera()
        elif cmd_opts.get("tilt") == "close":
            self.servo.close_camera()

        self.servo.cleanup()
