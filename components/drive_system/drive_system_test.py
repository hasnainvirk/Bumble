from components.drive_system.modules.drive_system import DriveSystem
from typing import TypedDict, Optional
import time


drive_system_cmd_options = TypedDict(
    "drive_system_cmd_options",
    {
        "forward": Optional[bool],
        "backward": Optional[bool],
        "left": Optional[bool],
        "right": Optional[bool],
    },
)


class DriveSystemTest(object):
    def __init__(self):
        self.__drive_system = DriveSystem()

    def execute_command(self, cmd_opts: drive_system_cmd_options):
        while True:
            time.sleep(0.01)
            try:
                if cmd_opts.get("forward"):
                    self.__drive_system.drive_forward()
                elif cmd_opts.get("backward"):
                    self.__drive_system.drive_backward()
                elif cmd_opts.get("left"):
                    self.__drive_system.turn_left()
                elif cmd_opts.get("right"):
                    self.__drive_system.turn_right()
                else:
                    self.__drive_system.stop()
                    break
            except KeyboardInterrupt:
                break

        self.__drive_system.stop()
