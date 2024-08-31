"""
Helper class to control the camera
"""

import logging
import threading
import queue
from typing import TypedDict, Optional, Dict
from components.servos.modules.camera_servo import CameraServo as camera_servo
from components.servos.modules.servo_iface import (
    SERVO_ID_ROTATION,
    SERVO_ID_TILT,
)


OPEN = "open"
CLOSE = "close"
LEFT = "left"
RIGHT = "right"
STRAIGHT = "straight"
UPWARD = "upward"
DOWNWARD = "downward"

cmds = TypedDict(
    "cmds",
    {
        "tilt": Optional[str],
        "point": Optional[str],
        "rotate_to_angle": Optional[Dict[str, int]],
    },
)


class CameraHelper:
    """
    Helper class to control the camera
    """

    def __init__(self):
        self.log = logging.getLogger("bumble")
        self.tilt_ctrl_servo = camera_servo(tid=SERVO_ID_TILT)
        self.rotate_servo = camera_servo(tid=SERVO_ID_ROTATION)
        self.queue = queue.Queue()
        self.thread = threading.Thread(
            target=self.__worker, daemon=False, name="Camera Helper"
        )
        self.clear_flag = threading.Event()

    def start(self):
        """
        Start the camera module
        shutdodown must be called to stop the module
        """

        self.thread.start()

    def shutdown(self):
        """
        Shutdown the camera module
        """
        cmd: cmds = {"tilt": CLOSE, "point": STRAIGHT, "rotate_to_angle": None}
        self.queue.put(cmd)
        self.queue.put(None)
        self.thread.join()

    def post_message(self, cmd_opts: cmds):
        """
        Post a message to the camera module
        """
        self.queue.put(cmd_opts)

    def __worker(self):
        while True:
            cmd_opts = self.queue.get()
            if cmd_opts is None:
                self.queue.task_done()
                break
            self.execute_command(cmd_opts)
            # block this thread until the clear flag is set
            self.clear_flag.wait()
            self.queue.task_done()

    def execute_command(self, cmd_opts: cmds):
        """
        Execute the command

        Args:
            cmd_opts: cmds: The command options
        """
        if cmd_opts.get("tilt"):
            if cmd_opts.get("tilt") == OPEN:
                self.tilt_ctrl_servo.open_camera()
            elif cmd_opts.get("tilt") == CLOSE:
                self.tilt_ctrl_servo.close_camera()
        elif cmd_opts.get("point"):
            if cmd_opts.get("point") == LEFT:
                self.rotate_servo.point_left()
            elif cmd_opts.get("point") == RIGHT:
                self.rotate_servo.point_right()
            elif cmd_opts.get("point") == STRAIGHT:
                self.rotate_servo.point_straight()
        elif cmd_opts.get("rotate_to_angle"):
            cmd_obj = cmd_opts.get("rotate_to_angle")
            if cmd_obj.get("direction") == LEFT or cmd_obj.get("direction") == RIGHT:
                self.rotate_servo.adjust_angle(
                    cmd_obj.get("angle"), cmd_obj.get("direction")
                )
            elif (
                cmd_obj.get("direction") == UPWARD
                or cmd_obj.get("direction") == DOWNWARD
            ):
                self.tilt_ctrl_servo.adjust_angle(
                    cmd_obj.get("angle"), cmd_obj.get("direction")
                )

        self.clear_flag.set()
