from components.servos.modules.camera_tilt_servo import (
    CameraTiltServo as camera_tilt_servo,
)
import logging
from typing import TypedDict, Optional


class CameraTiltServoTest:
    def __init__(self):
        self.servo = camera_tilt_servo()
        self.log = logging.getLogger("bumble")

    def execute_command(self, cmd_opts):
        if cmd_opts.get("tilt") == "close":
            self.servo.close_camera()
        elif cmd_opts.get("tilt") == "open":
            self.servo.open_camera()
        else:
            raise ValueError("Invalid command options")
