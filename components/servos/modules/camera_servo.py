"""
Camera Servo module
"""

from components.servos.modules.servo_iface import (
    ServoIface,
    SERVO_ID_TILT,
)

# constants
GPIO_6 = 6  # GPIO pin for camera tilt servo
GPIO_7 = 7  # GPIO pin for camera rotation servo

ROTATE_UPWARD = "upward"
ROTATE_DOWNWARD = "downward"


class CameraServo(ServoIface):
    """
    Camera Servo class

    Inherits from ServoIface

    Args:
        tid (int, optional): Servo ID. Defaults to None.
        [options: SERVO_ID_ROTATION=1, SERVO_ID_TILT=0]
    """

    def __init__(self, tid: int = None):
        if tid == SERVO_ID_TILT:
            super().__init__(gpio_pin=GPIO_6, name="Camera Tilt Servo", tid=tid)
            super().close_camera()
        else:
            super().__init__(gpio_pin=GPIO_7, name="Camera Rotation Servo", tid=tid)
            super().point_straight()
