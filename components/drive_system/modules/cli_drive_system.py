from components.wheels.modules.lower_left_wheel import LowerLeftWheel
from components.wheels.modules.lower_right_wheel import LowerRightWheel
from components.wheels.modules.upper_left_wheel import UpperLeftWheel
from components.wheels.modules.upper_right_wheel import UpperRightWheel


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


class CliDriveSystem:
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
        self.speed = 30
        self.wheel: WheelIface = None
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            self.wheel.set_speed(self.speed)

    def drive_forward(self):
        self.__drive(DIRECTION_FORWARD)

    def drive_backward(self):
        self.__drive(DIRECTION_BACKWARD)

    def stop(self):
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            self.wheel.stop()

    def cleanup(self):
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            self.wheel.cleanup()

    def turn_left(self):
        self.wheel = self.__ctrl.get(UPPER_LEFT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_backwards()

        self.wheel = self.__ctrl.get(LOWER_LEFT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_backwards()

        self.wheel = self.__ctrl.get(UPPER_RIGHT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_forward()

        self.wheel = self.__ctrl.get(LOWER_RIGHT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_forward()

    def turn_right(self):
        self.wheel = self.__ctrl.get(UPPER_LEFT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_forward()

        self.wheel = self.__ctrl.get(LOWER_LEFT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_forward()

        self.wheel = self.__ctrl.get(UPPER_RIGHT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_backwards()

        self.wheel = self.__ctrl.get(LOWER_RIGHT_WHEEL)
        self.wheel.set_speed(self.speed)
        self.wheel.move_backwards()

    def __drive(self, direction: str):
        for wheel in self.__wheels:
            self.wheel = self.__ctrl.get(wheel)
            self.wheel.set_speed(self.speed)
            if direction == DIRECTION_FORWARD:
                self.wheel.move_forward()
            elif direction == DIRECTION_BACKWARD:
                self.wheel.move_backwards()
