import RPi.GPIO as GPIO
from component_testing.wheels.modules.wheel_iface import (
    WheelIface,
    wheel_status,
    WHEEL_MOVING_FORWARD,
    WHEEL_MOVING_BACKWARD,
    WHEEL_STOPPED,
    UPPER_RIGHT_WHEEL,
)


GPIO.setwarnings(False)


class UpperRightWheel(WheelIface):
    def __init__(self):
        self.__name = UPPER_RIGHT_WHEEL
        self.__speed = 0
        self.__pwm = None
        # GPIO_12 = PWM1, GPIO_24 = AIN1, GPIO_25 = AIN2
        self.__gpio_pins = {"GPIO_12": 12, "GPIO_24": 24, "GPIO_25": 25}
        self.__get_wheel_ready()

    def set_speed(self, speed: int):
        self.__set_duty_cycle(speed)

    def get_speed(self):
        return self.__speed

    def get_name(self):
        return self.__name

    def move_forward(self) -> wheel_status:
        GPIO.output(self.__gpio_pins.get("GPIO_24"), GPIO.HIGH)  # Upper Right forward
        GPIO.output(self.__gpio_pins.get("GPIO_25"), GPIO.LOW)
        self.__set_duty_cycle(80)
        status: wheel_status = {
            "name": self.__name,
            "speed": self.__speed,
            "retcode": WHEEL_MOVING_FORWARD,
        }
        return status

    def move_backwards(self) -> wheel_status:
        GPIO.output(self.__gpio_pins.get("GPIO_24"), GPIO.LOW)  # Upper Left backwards
        GPIO.output(self.__gpio_pins.get("GPIO_25"), GPIO.HIGH)
        self.__set_duty_cycle(80)
        status: wheel_status = {
            "name": self.__name,
            "speed": self.__speed,
            "retcode": WHEEL_MOVING_BACKWARD,
        }
        return status

    def stop(self) -> wheel_status:
        self.__set_duty_cycle(0)
        status: wheel_status = {
            "name": self.__name,
            "speed": self.__speed,
            "retcode": WHEEL_STOPPED,
        }
        return status

    def __get_wheel_ready(self):
        GPIO.setmode(GPIO.BCM)
        # set the MOTOR Driver Pin OUTPUT mode
        GPIO.setup(self.__gpio_pins.get("GPIO_24"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_25"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_12"), GPIO.OUT)
        self.__pwm = GPIO.PWM(self.__gpio_pins.get("GPIO_12"), 100)
        self.__pwm.start(0)  # set inital duty cycle to 0

    def __set_duty_cycle(self, speed: int):
        self.__pwm.ChangeDutyCycle(speed)
        self.__speed = speed
