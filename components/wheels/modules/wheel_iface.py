"""
This module is responsible for providing a common interface for the wheels of the robot.
"""

import abc
from typing import TypedDict, Optional

WHEEL_MOVING_FORWARD = 100
WHEEL_MOVING_BACKWARD = 200
WHEEL_STOPPED = 300

UPPER_LEFT_WHEEL = "upper_left"
LOWER_LEFT_WHEEL = "lower_left"
UPPER_RIGHT_WHEEL = "upper_right"
LOWER_RIGHT_WHEEL = "lower_right"
DIRECTION_FORWARD = "forward"
DIRECTION_BACKWARD = "backward"
DIRECTION_LEFT = "left"
DIRECTION_RIGHT = "right"
DIRECTION_NONE = "none"

wheel_msg_action = TypedDict(
    "wheel_msg_action",
    {
        "direction": str,
        "speed": int,
        "name": Optional[str],
        "slow_down": bool,
        "delay": Optional[float],
        "step": Optional[int],
    },
)

wheel_message = TypedDict(
    "wheel_message",
    {
        UPPER_LEFT_WHEEL: wheel_msg_action,
        LOWER_LEFT_WHEEL: wheel_msg_action,
        UPPER_RIGHT_WHEEL: wheel_msg_action,
        LOWER_RIGHT_WHEEL: wheel_msg_action,
    },
)


class WheelIface(metaclass=abc.ABCMeta):
    """
    Abstract class to provide a common interface binding for Wheels of the robot.
    Children must implement abstract methods.
    """

    wheel = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "move_forward", "move_backwards", "stop") and callable(
            subclass.move_forward, subclass.move_backwards, subclass.stop
        )

    @abc.abstractmethod
    def move_forward(self):
        """
        Move the wheel forward
        """
        raise NotImplementedError

    @abc.abstractmethod
    def move_backwards(self):
        """
        Move the wheel backwards
        """
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        """
        Stop the wheel
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_speed(self, speed: int):
        """
        Set the speed of the wheel
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_speed(self) -> int:
        """
        Get the speed of the wheel
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the wheel
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cleanup(self) -> str:
        """
        Clean up the wheel
        """
        raise NotImplementedError


wheel_ctrl_options = TypedDict(
    "wheel_ctrl_options",
    {
        # object to control the upper left wheel
        "upper_left": Optional[WheelIface],
        # object to control the lower left wheel
        "lower_left": Optional[WheelIface],
        # object to control the upper right wheel
        "upper_right": Optional[WheelIface],
        # object to control the lower right wheel
        "lower_right": Optional[WheelIface],
    },
)
