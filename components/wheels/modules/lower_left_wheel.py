"""
Lower Left Wheel Module
"""

import logging
import time
import RPi.GPIO as GPIO

from components.wheels.modules.wheel_iface import (
    WheelIface,
    wheel_msg_action,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    DIRECTION_NONE,
    LOWER_LEFT_WHEEL,
)


GPIO.setwarnings(False)


class LowerLeftWheel(WheelIface):
    """
    Lower Left Wheel class
    """

    def __init__(self):
        super().__init__()
        self.__name = LOWER_LEFT_WHEEL
        self.__speed = 0
        self.__pwm = None
        # GPIO_1 = PWM1, GPIO_22 = BIN1, GPIO_23 = BIN2
        self.__gpio_pins = {"GPIO_1": 1, "GPIO_22": 22, "GPIO_23": 23}
        self.__get_wheel_ready()
        self.log = logging.getLogger("bumble")

    def set_speed(self, speed: int):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def get_name(self):
        return self.__name

    def move_forward(self):
        GPIO.output(self.__gpio_pins.get("GPIO_22"), GPIO.HIGH)  # Lower Left forward
        GPIO.output(self.__gpio_pins.get("GPIO_23"), GPIO.LOW)
        self.__set_duty_cycle(self.__speed)

    def move_backwards(self):
        GPIO.output(self.__gpio_pins.get("GPIO_22"), GPIO.LOW)  # Upper Left backwards
        GPIO.output(self.__gpio_pins.get("GPIO_23"), GPIO.HIGH)
        self.__set_duty_cycle(self.__speed)

    def stop(self):
        self.__set_duty_cycle(0)

    def gradually_decrease_speed(self, step=5, delay=0.1):
        """
        Gradually decrease the speed of the motor

        Args:
            step (int): The amount by which to decrease the speed
            delay (float): The delay between each decrease in speed
        """
        while self.__speed > 0:
            self.__speed -= step
            if self.__speed < 0:
                self.__speed = 0
            self.__set_duty_cycle(self.__speed)
            time.sleep(delay)
        self.__set_duty_cycle(0)  # Ensure the motor is completely stopped

    def process_message(self, action: wheel_msg_action):
        """
        Process the message received by the wheel

        Args:
            action (wheel_msg_action): The action to be performed by the wheel
            direction (str): The direction in which the wheel should move
            speed (int): The speed at which the wheel should move
            name (str): The name of the wheel
            slow_down (bool): Flag to indicate if the wheel should gradually decrease speed
            delay (float): The delay between each decrease in speed
            step (int): The amount by which to decrease the speed
        """
        if action["name"] == self.__name:
            self.__speed = action["speed"]
            if action["direction"] == DIRECTION_FORWARD:
                self.move_forward()
            elif action["direction"] == DIRECTION_BACKWARD:
                self.move_backwards()
            elif action["direction"] == DIRECTION_NONE:
                self.stop()

        if action["slow_down"] is True and self.__speed != 0:
            self.gradually_decrease_speed(step=action["step"], delay=action["delay"])

        self.log.debug("Wheel %s processed message: %s", self.__name, action)

    def cleanup(self):
        self.__set_duty_cycle(0)
        self.__pwm.stop()
        GPIO.cleanup(
            [
                self.__gpio_pins.get("GPIO_1"),
                self.__gpio_pins.get("GPIO_22"),
                self.__gpio_pins.get("GPIO_23"),
            ]
        )

    def __get_wheel_ready(self):
        GPIO.setmode(GPIO.BCM)
        # set the MOTOR Driver Pin OUTPUT mode
        GPIO.setup(self.__gpio_pins.get("GPIO_22"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_23"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("GPIO_1"), GPIO.OUT)
        self.__pwm = GPIO.PWM(self.__gpio_pins.get("GPIO_1"), 100)
        self.__pwm.start(0)  # set inital duty cycle to 0

    def __set_duty_cycle(self, speed: int):
        self.__pwm.ChangeDutyCycle(speed)
        self.__speed = speed
