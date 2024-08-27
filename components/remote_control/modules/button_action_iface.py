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
        raise NotImplementedError

    @abc.abstractmethod
    def down(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def right(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def left(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def ok(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def zero(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def one(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def two(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def three(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def four(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def five(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def six(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def seven(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def eight(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def nine(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def asterisk(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def hash(self, **kwargs):
        raise NotImplementedError
