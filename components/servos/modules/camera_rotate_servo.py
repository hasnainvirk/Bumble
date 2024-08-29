from components.servos.modules.servo_iface import ServoIface
import logging

GPIO_7 = 7
POINTING_STRAIGHT_ANGLE = 90
POINTING_RIGHT_ANGLE = 0
POINTING_LEFT_ANGLE = 180


class CameraRotateServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_7)
        self.log = logging.getLogger("bumble")
        self.current_angle = POINTING_STRAIGHT_ANGLE
        self.point_straight()

    def point_straight(self):
        self.log.debug("Camera Servo - Point straight")
        # try many times to make sure the servo is at pointing straight at 90 degrees
        self.generate_pulse(POINTING_STRAIGHT_ANGLE)
        # for _ in range(0, 50):
        #     self.generate_pulse(POINTING_STRAIGHT_ANGLE)
        # self.__set_angle(POINTING_STRAIGHT_ANGLE)

    def point_right(self):
        self.log.debug("Camera Servo - Point Right")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_RIGHT_ANGLE)
        self.__set_angle(POINTING_RIGHT_ANGLE)

    def point_left(self):
        self.log.debug("Camera Servo - Piont Left")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_LEFT_ANGLE)
        self.__set_angle(POINTING_LEFT_ANGLE)

    def rotate_right(self):
        self.log.debug("Camera Servo - Rotating Right")
        i = self.current_angle
        while i >= POINTING_RIGHT_ANGLE:
            self.generate_pulse(i)
            i -= 1
        self.__set_angle(i)

    def rotate_left(self):
        self.log.debug("Camera Servo - Rotating Left")
        i = self.current_angle
        while i <= POINTING_LEFT_ANGLE:
            self.generate_pulse(i)
            i += 1
        self.__set_angle(i)

    def rotate_to_angle(self, angle: int):
        self.log.debug(f"Camera Servo - Rotating to {angle} degrees")
        i = self.current_angle
        if i > angle:
            while i >= angle:
                self.generate_pulse(i)
                i -= 1
        elif i < angle:
            while i <= angle:
                self.generate_pulse(i)
                i += 1
        elif i == angle:
            return

        self.__set_angle(i)

    def rotate_center(self):
        self.log.debug("Camera Servo - Rotating to Center")
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
