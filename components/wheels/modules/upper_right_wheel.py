import RPi.GPIO as GPIO
import logging, time
from components.wheels.modules.wheel_iface import (
    WheelIface,
    wheel_msg_action,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    DIRECTION_NONE,
    UPPER_RIGHT_WHEEL,
)


GPIO.setwarnings(False)


class UpperRightWheel(WheelIface):
    def __init__(self):
        super().__init__()
        self.__name = UPPER_RIGHT_WHEEL
        self.__speed = 0
        self.__pwm = None
        # GPIO_12 = PWM1, GPIO_24 = AIN1, GPIO_25 = AIN2
        self.__gpio_pins = {"GPIO_12": 12, "GPIO_24": 24, "GPIO_25": 25}
        self.__get_wheel_ready()
        self.log = logging.getLogger("bumble")

    def set_speed(self, speed: int):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def get_name(self):
        return self.__name

    def move_forward(self, duration=None):
        GPIO.output(self.__gpio_pins.get("GPIO_24"), GPIO.HIGH)  # Upper Right forward
        GPIO.output(self.__gpio_pins.get("GPIO_25"), GPIO.LOW)
        self.__set_duty_cycle(self.__speed)

    def move_backwards(self, duration=None):
        GPIO.output(self.__gpio_pins.get("GPIO_24"), GPIO.LOW)  # Upper Left backwards
        GPIO.output(self.__gpio_pins.get("GPIO_25"), GPIO.HIGH)
        self.__set_duty_cycle(self.__speed)

    def stop(self):
        self.__set_duty_cycle(0)

    def gradually_decrease_speed(self, step=5, delay=0.1):
        while self.__speed > 0:
            self.__speed -= step
            if self.__speed < 0:
                self.__speed = 0
            self.__set_duty_cycle(self.__speed)
            time.sleep(delay)
        self.__set_duty_cycle(0)  # Ensure the motor is completely stopped

    def process_message(self, action: wheel_msg_action):
        if action["name"] == self.__name:
            self.__speed = action["speed"]
            if action["direction"] == DIRECTION_FORWARD:
                self.move_forward()
            elif action["direction"] == DIRECTION_BACKWARD:
                self.move_backwards()
            elif action["direction"] == DIRECTION_NONE:
                self.stop()

        if action["slow_down"] == True and self.__speed != 0:
            self.gradually_decrease_speed(step=action["step"], delay=action["delay"])

        self.log.debug(f"Wheel {self.__name} processed message: {action}")

    def cleanup(self):
        self.__set_duty_cycle(0)
        self.__pwm.stop()
        GPIO.cleanup(
            [
                self.__gpio_pins.get("GPIO_12"),
                self.__gpio_pins.get("GPIO_24"),
                self.__gpio_pins.get("GPIO_25"),
            ]
        )

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
