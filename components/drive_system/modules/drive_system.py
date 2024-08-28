from components.wheels.modules.lower_left_wheel import LowerLeftWheel
from components.wheels.modules.lower_right_wheel import LowerRightWheel
from components.wheels.modules.upper_left_wheel import UpperLeftWheel
from components.wheels.modules.upper_right_wheel import UpperRightWheel
import time

from components.wheels.modules.wheel_iface import (
    wheel_ctrl_options,
    WheelIface,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    UPPER_LEFT_WHEEL,
    LOWER_LEFT_WHEEL,
    UPPER_RIGHT_WHEEL,
    LOWER_RIGHT_WHEEL,
)


class DriveSystem:
    def __init__(self):
        self.__ctrl: wheel_ctrl_options = {}
        self.__ctrl.update({UPPER_LEFT_WHEEL: UpperLeftWheel()})
        self.__ctrl.update({LOWER_LEFT_WHEEL: LowerLeftWheel()})
        self.__ctrl.update({UPPER_RIGHT_WHEEL: UpperRightWheel()})
        self.__ctrl.update({LOWER_RIGHT_WHEEL: LowerRightWheel()})
        self.__wheels = [
            UPPER_LEFT_WHEEL,
            LOWER_LEFT_WHEEL,
            UPPER_RIGHT_WHEEL,
            LOWER_RIGHT_WHEEL,
        ]
        self.wheel: WheelIface = None

    def drive_forward(self, duration=None):
        self.__drive(DIRECTION_FORWARD, duration)

    def drive_backward(self):
        self.__drive(DIRECTION_BACKWARD)

    def stop(self):
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            self.wheel.stop()

    def turn_left(self, duration=None):
        self.__ctrl.get(UPPER_LEFT_WHEEL).move_backwards(duration=duration)
        self.__ctrl.get(LOWER_LEFT_WHEEL).move_backwards(duration=duration)
        self.__ctrl.get(UPPER_RIGHT_WHEEL).move_forward(duration=duration)
        self.__ctrl.get(LOWER_RIGHT_WHEEL).move_forward(duration=duration)

    def turn_right(self, duration=None):
        self.__ctrl.get(UPPER_LEFT_WHEEL).move_forward(duration=duration)
        self.__ctrl.get(LOWER_LEFT_WHEEL).move_forward(duration=duration)
        self.__ctrl.get(UPPER_RIGHT_WHEEL).move_backwards(duration=duration)
        self.__ctrl.get(LOWER_RIGHT_WHEEL).move_backwards(duration=duration)

    def __drive(self, direction: str, duration=None):
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            if direction == DIRECTION_FORWARD:
                self.wheel.move_forward(duration=duration)
            elif direction == DIRECTION_BACKWARD:
                self.wheel.move_backwards(duration=duration)
