from components.servos.modules.servo_iface import ServoIface
import RPi.GPIO as GPIO
import time, logging

GPIO_6 = 6
CLOSE_CAMERA_ANGLE = 0
OPEN_CAMERA_ANGLE = 90


class CameraTiltServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_6)
        self.log = logging.getLogger("bumble")

    def close_camera(self):
        self.log.debug("Camera Servo - Closing Camera")
        for _ in range(0, 50):
            self.generate_pulse(CLOSE_CAMERA_ANGLE)

    def open_camera(self):
        self.log.debug("Camera Servo - Opening Camera")
        for _ in range(0, 50):
            self.generate_pulse(OPEN_CAMERA_ANGLE)
