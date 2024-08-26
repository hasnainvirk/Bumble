from components.servos.modules.servo_iface import ServoIface
import RPi.GPIO as GPIO
import time, logging

GPIO_6 = 6
POINTING_CENTER_ANGLE = 90
POINTING_DOWN_ANGLE = 180
POINTING_UP_ANGLE = 0


class CameraTiltServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_6)
        self.log = logging.getLogger("bumble")
        self.current_angle = POINTING_DOWN_ANGLE
        self.tilt_down()

    def tilt_center(self):
        self.log.debug("Camera Servo - Tilting Center")
        self.generate_pulse(POINTING_DOWN_ANGLE)
        self.__set_angle(POINTING_DOWN_ANGLE)

    def tilt_down(self):
        self.log.debug("Camera Servo - Tilting Down")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_DOWN_ANGLE)

    def tilt_up(self):
        self.log.debug("Camera Servo - Tilting Up")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_UP_ANGLE)

    def __set_angle(self, angle):
        self.current_angle = angle
