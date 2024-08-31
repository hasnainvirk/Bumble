"""
Line Tracking Sensor Module
"""

from typing import TypedDict
import logging
import RPi.GPIO as GPIO

from components.wheels.modules.wheel_iface import (
    DIRECTION_FORWARD,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_NONE,
)

line_ctrl = TypedDict(
    "line_ctrl",
    {
        "right": int,
        "middle": int,
        "left": int,
        "decision": str,
    },
)


class LineTrackingSensor:
    """
    Line Tracking Sensor class
    """

    def __init__(self):
        self.__gpio_pins = {"GPIO_17": 17, "GPIO_18": 18, "GPIO_19": 19}
        self.__setup()
        self.log = logging.getLogger("bumble")

    def read(self) -> line_ctrl:
        """
        Reads the line tracking sensor and returns the decision based on the sensor readings
        """
        return self.__get_decision()

    def cleanup(self):
        """
        Cleans up the GPIO pins
        """
        GPIO.cleanup(
            [
                self.__gpio_pins["GPIO_17"],
                self.__gpio_pins["GPIO_18"],
                self.__gpio_pins["GPIO_19"],
            ]
        )

    def __get_decision(self) -> line_ctrl:
        right = GPIO.input(self.__gpio_pins["GPIO_17"])
        middle = GPIO.input(self.__gpio_pins["GPIO_18"])
        left = GPIO.input(self.__gpio_pins["GPIO_19"])

        self.log.debug("Right: %s, Middle: %s, Left: %s", right, middle, left)

        if middle == 1:
            return {"right": 0, "middle": 1, "left": 0, "decision": DIRECTION_FORWARD}
        else:
            if right == 1 and left == 0:
                return {"right": 1, "middle": 0, "left": 0, "decision": DIRECTION_RIGHT}
            elif right == 0 and left == 1:
                return {"right": 0, "middle": 0, "left": 1, "decision": DIRECTION_LEFT}
            else:
                return {"right": 0, "middle": 0, "left": 0, "decision": DIRECTION_NONE}

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.__gpio_pins.values():
            GPIO.setup(pin, GPIO.IN)
