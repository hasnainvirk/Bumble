"""
Clas to test the drive system module
"""

from typing import TypedDict, Optional
import time
from components.drive_system.modules.cli_drive_system import (
    CliDriveSystem as drive_system,
)


drive_system_cmd_options = TypedDict(
    "drive_system_cmd_options",
    {
        "forward": Optional[bool],
        "backward": Optional[bool],
        "left": Optional[bool],
        "right": Optional[bool],
    },
)


class DriveSystemTest:
    """
    Class to test the drive system module
    """

    def __init__(self):
        self.__drive_system = drive_system()

    def execute_command(self, cmd_opts: drive_system_cmd_options):
        """
        Executes the command based on the given options

        Args:
            cmd_opts (drive_system_cmd_options): A dictionary containing the command options.
                - forward (Optional[bool]): Drive the robot forward.
                - backward (Optional[bool]): Drive the robot backward.
                - left (Optional[bool]): Turn the robot left.
                - right (Optional[bool]): Turn the robot right.
        """
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
        self.__drive_system.cleanup()
