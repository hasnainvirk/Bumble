import time
from typing import TypedDict, Optional
from components.wheels.modules.upper_left_wheel import UpperLeftWheel
from components.wheels.modules.lower_left_wheel import LowerLeftWheel
from components.wheels.modules.upper_right_wheel import UpperRightWheel
from components.wheels.modules.lower_right_wheel import LowerRightWheel
from components.wheels.modules.wheel_iface import (
    wheel_ctrl_options,
    WheelIface,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    DIRECTION_NONE,
    UPPER_LEFT_WHEEL,
    LOWER_LEFT_WHEEL,
    UPPER_RIGHT_WHEEL,
    LOWER_RIGHT_WHEEL,
)

wheel_cmd_options = TypedDict(
    "wheel_cmd_options",
    {
        "forward": Optional[str],
        "backward": Optional[str],
    },
)


class WheelsTest(object):
    def __init__(self):
        self.__ctrl: wheel_ctrl_options = {}
        self.__ctrl.update({UPPER_LEFT_WHEEL: UpperLeftWheel()})
        self.__ctrl.update({LOWER_LEFT_WHEEL: LowerLeftWheel()})
        self.__ctrl.update({UPPER_RIGHT_WHEEL: UpperRightWheel()})
        self.__ctrl.update({LOWER_RIGHT_WHEEL: LowerRightWheel()})
        self.wheel: WheelIface = None

    def execute_command(self, cmd_opts: wheel_cmd_options):

        if cmd_opts.get("forward"):
            self.__handle_wheel(cmd_opts.get("forward"), DIRECTION_FORWARD)
        elif cmd_opts.get("backward"):
            self.__handle_wheel(cmd_opts.get("backward"), DIRECTION_BACKWARD)

    def __handle_wheel(self, wheel_name: str, direction: str):
        self.wheel = self.__ctrl.get(wheel_name)
        if not self.wheel:
            raise ValueError(f"Invalid wheel name: {wheel_name}")
        self.wheel.set_speed(100)
        while True:
            time.sleep(0.01)
            try:
                if direction == DIRECTION_FORWARD:
                    self.wheel.move_forward()
                elif direction == DIRECTION_BACKWARD:
                    self.wheel.move_backwards()
                elif direction == DIRECTION_NONE:
                    self.wheel.stop()
                    break
                else:
                    raise ValueError(f"Invalid direction: {direction}")
            except KeyboardInterrupt:
                self.wheel.stop()
                break
