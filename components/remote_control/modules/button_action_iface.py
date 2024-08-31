"""
ButtonActionIface module provides an abstract class to provide a common interface binding 
for Buttons of the IR remote control.
"""

import abc


class ButtonActionIface(metaclass=abc.ABCMeta):
    """
    Abstract class to provide a common interface binding for Buttons of the IR remote control.
    Children must implement abstract methods.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(
            subclass,
            "up",
            "down",
            "right",
            "left",
            "ok",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "asterisk",
            "hash",
        ) and callable(
            subclass.up,
            subclass.down,
            subclass.right,
            subclass.left,
            subclass.ok,
            subclass.one,
            subclass.two,
            subclass.three,
            subclass.four,
            subclass.five,
            subclass.six,
            subclass.seven,
            subclass.eight,
            subclass.nine,
            subclass.asterisk,
            subclass.hash,
        )

    @abc.abstractmethod
    def up(self, **kwargs):
        """
        Abstract method to handle the up button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def down(self, **kwargs):
        """
        Abstract method to handle the down button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def right(self, **kwargs):
        """
        Abstract method to handle the right button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def left(self, **kwargs):
        """
        Abstract method to handle the left button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def ok(self, **kwargs):
        """
        Abstract method to handle the ok button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def zero(self, **kwargs):
        """
        Abstract method to handle the zero button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def one(self, **kwargs):
        """
        Abstract method to handle the one button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def two(self, **kwargs):
        """
        Abstract method to handle the two button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def three(self, **kwargs):
        """
        Abstract method to handle the three button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def four(self, **kwargs):
        """
        Abstract method to handle the four button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def five(self, **kwargs):
        """
        Abstract method to handle the five button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def six(self, **kwargs):
        """
        Abstract method to handle the six button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def seven(self, **kwargs):
        """
        Abstract method to handle the seven button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def eight(self, **kwargs):
        """
        Abstract method to handle the eight button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def nine(self, **kwargs):
        """
        Abstract method to handle the nine button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def asterisk(self, **kwargs):
        """
        Abstract method to handle the asterisk button action.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def hash(self, **kwargs):
        """
        Abstract method to handle the hash button action.
        """
        raise NotImplementedError
