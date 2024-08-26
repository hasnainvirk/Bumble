from components.servos.modules.servo_iface import ServoIface
import RPi.GPIO as GPIO
import time, logging

GPIO_6 = 6
POINTING_STRAIGHT_ANGLE = 90
POINTING_DOWN_ANGLE = 0
POINTING_UP_ANGLE = 180


class CameraTiltServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_6)
        self.log = logging.getLogger("bumble")
        self.current_angle = POINTING_STRAIGHT_ANGLE
        self.point_straight()

    def point_straight(self):
        self.log.debug("Camera Servo - Point straight")
        # try many times to make sure the servo is at pointing straight at 90 degrees
        for _ in range(0, 50):
            self.generate_pulse(POINTING_STRAIGHT_ANGLE)
        self.__set_angle(POINTING_STRAIGHT_ANGLE)

    def point_down(self):
        self.log.debug("Camera Servo - Point Down")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_DOWN_ANGLE)
        self.__set_angle(POINTING_DOWN_ANGLE)

    def point_up(self):
        self.log.debug("Camera Servo - Piont Up")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_UP_ANGLE)
        self.__set_angle(POINTING_UP_ANGLE)

    def tilt_down(self):
        self.log.debug("Camera Servo - Tilting Right")
        i = self.current_angle
        while i >= POINTING_STRAIGHT_ANGLE:
            self.generate_pulse(i)
            i -= 1
        self.__set_angle(i)

    def tilt_up(self):
        self.log.debug("Camera Servo - Tilting Left")
        i = self.current_angle
        while i <= POINTING_UP_ANGLE:
            self.generate_pulse(i)
            i += 1
        self.__set_angle(i)

    def tilt_center(self):
        self.log.debug("Camera Servo - Tilting to Center")
        i = self.current_angle
        if i > POINTING_STRAIGHT_ANGLE:
            while i >= POINTING_STRAIGHT_ANGLE:
                self.generate_pulse(i)
                i -= 1
        elif i < POINTING_STRAIGHT_ANGLE:
            while i <= POINTING_STRAIGHT_ANGLE:
                self.generate_pulse(i)
                i += 1
        elif i == POINTING_STRAIGHT_ANGLE:
            return

        self.__set_angle(i)

    def __set_angle(self, angle):
        self.current_angle = angle
