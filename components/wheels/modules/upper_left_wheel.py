import RPi.GPIO as GPIO
from components.wheels.modules.wheel_iface import (
    WheelIface,
    UPPER_LEFT_WHEEL,
)


GPIO.setwarnings(False)


class UpperLeftWheel(WheelIface):
    def __init__(self):
        self.__name = UPPER_LEFT_WHEEL
        self.__speed = 0
        self.__pwm = None
        # GPIO_0 = PWM1, GPIO_20 = AIN1, GPIO_21 = AIN2
        self.__gpio_pins = {"GPIO_0": 0, "GPIO_20": 20, "GPIO_21": 21}
        self.__get_wheel_ready()

    def set_speed(self, speed: int):
        self.__set_duty_cycle(speed)

    def get_speed(self):
        return self.__speed

    def get_name(self):
        return self.__name

    def move_forward(self):
        GPIO.output(self.__gpio_pins.get("GPIO_20"), GPIO.LOW)  # Upper Left forward
        GPIO.output(self.__gpio_pins.get("GPIO_21"), GPIO.HIGH)
        self.__set_duty_cycle(80)

    def move_backwards(self):
        GPIO.output(self.__gpio_pins.get("GPIO_20"), GPIO.HIGH)  # Upper Left backwards
        GPIO.output(self.__gpio_pins.get("GPIO_21"), GPIO.LOW)
        self.__set_duty_cycle(80)

    def stop(self):
        self.__set_duty_cycle(0)

    def __get_wheel_ready(self):
        GPIO.setmode(GPIO.BCM)
        # set the MOTOR Driver Pin OUTPUT mode
        GPIO.setup(self.__gpio_pins.get("GPIO_20"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_21"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_0"), GPIO.OUT)
        self.__pwm = GPIO.PWM(self.__gpio_pins.get("GPIO_0"), 100)
        self.__pwm.start(0)  # set inital duty cycle to 0

    def __set_duty_cycle(self, speed: int):
        self.__pwm.ChangeDutyCycle(speed)
        self.__speed = speed
