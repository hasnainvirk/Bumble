import RPi.GPIO as GPIO
from components.wheels.modules.wheel_iface import (
    WheelIface,
    LOWER_RIGHT_WHEEL,
)


GPIO.setwarnings(False)


class LowerRightWheel(WheelIface):
    def __init__(self):
        self.__name = LOWER_RIGHT_WHEEL
        self.__speed = 0
        self.__pwm = None
        # GPIO_13 = PWM1, GPIO_26 = BIN1, GPIO_27 = BIN2
        self.__gpio_pins = {"GPIO_13": 13, "GPIO_26": 26, "GPIO_27": 27}
        self.__get_wheel_ready()

    def set_speed(self, speed: int):
        self.__set_duty_cycle(speed)

    def get_speed(self):
        return self.__speed

    def get_name(self):
        return self.__name

    def move_forward(self):
        GPIO.output(self.__gpio_pins.get("GPIO_26"), GPIO.LOW)  # Lower right forward
        GPIO.output(self.__gpio_pins.get("GPIO_27"), GPIO.HIGH)
        self.__set_duty_cycle(80)

    def move_backwards(self):
        GPIO.output(self.__gpio_pins.get("GPIO_26"), GPIO.HIGH)  # Lower Right backwards
        GPIO.output(self.__gpio_pins.get("GPIO_27"), GPIO.LOW)
        self.__set_duty_cycle(80)

    def stop(self):
        self.__set_duty_cycle(0)

    def __get_wheel_ready(self):
        GPIO.setmode(GPIO.BCM)
        # set the MOTOR Driver Pin OUTPUT mode
        GPIO.setup(self.__gpio_pins.get("GPIO_26"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_27"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_13"), GPIO.OUT)
        self.__pwm = GPIO.PWM(self.__gpio_pins.get("GPIO_13"), 100)
        self.__pwm.start(0)  # set inital duty cycle to 0

    def __set_duty_cycle(self, speed: int):
        self.__pwm.ChangeDutyCycle(speed)
        self.__speed = speed
