import time
from component_testing.wheels.modules.upper_left_wheel import UpperLeftWheel
from component_testing.wheels.modules.lower_left_wheel import LowerLeftWheel
from component_testing.wheels.modules.upper_right_wheel import UpperRightWheel
from component_testing.wheels.modules.lower_right_wheel import LowerRightWheel
from component_testing.wheels.modules.wheel_iface import (
    wheel_cmd_options,
    wheel_ctrl_options,
    WheelIface,
    wheel_status,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    DIRECTION_NONE,
    UPPER_LEFT_WHEEL,
    LOWER_LEFT_WHEEL,
    UPPER_RIGHT_WHEEL,
    LOWER_RIGHT_WHEEL,
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
        elif cmd_opts.get("stop"):
            self.__handle_wheel(cmd_opts.get("stop"), DIRECTION_NONE)

    def __handle_wheel(self, wheel_name: str, direction: str) -> wheel_status:
        self.wheel = self.__ctrl.get(wheel_name)
        if not self.wheel:
            raise ValueError(f"Invalid wheel name: {wheel_name}")

        self.__ctrl.update({f"{wheel_name}_dir": direction})

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
