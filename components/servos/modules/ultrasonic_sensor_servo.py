from components.servos.modules.servo_iface import ServoIface
import RPi.GPIO as GPIO
import time, logging

GPIO_5 = 5
POINTING_STRAIGHT_ANGLE = 90
POINTING_RIGHT_ANGLE = 0
POINTING_LEFT_ANGLE = 180


class UltrasonicSensorServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_5)
        self.log = logging.getLogger("bumble")

    def point_straight(self):
        self.log.debug("Ultrasonic Servo - Point straight")
        # try many times to make sure the servo is at pointing straight at 90 degrees
        for _ in range(0, 50):
            self.generate_pulse(POINTING_STRAIGHT_ANGLE)

    def turn_right(self):
        self.log.debug("Ultrasonic Servo - Turn Right")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_RIGHT_ANGLE)

    def turn_left(self):
        self.log.debug("Ultrasonic Servo - Turn Left")
        for _ in range(0, 50):
            self.generate_pulse(POINTING_LEFT_ANGLE)
