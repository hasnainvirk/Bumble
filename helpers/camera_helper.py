from components.servos.modules.camera_tilt_servo import (
    CameraTiltServo as camera_tilt_servo,
)
from components.servos.modules.camera_rotate_servo import (
    CameraRotateServo as camera_rotation_servo,
)
import logging, threading, queue
from typing import TypedDict, Optional

OPEN = "open"
CLOSE = "close"
LEFT = "left"
RIGHT = "right"
STRAIGHT = "straight"

cmds = TypedDict(
    "cmds",
    {
        "tilt": Optional[str],
        "point": Optional[str],
        "totate_to_angle": Optional[int],
    },
)


class CameraHelper:
    def __init__(self):
        self.tilt_servo = camera_tilt_servo()
        self.rotate_servo = camera_rotation_servo()
        self.log = logging.getLogger("bumble")
        self.queue = queue.Queue()
        self.thread = threading.Thread(
            target=self.__worker, daemon=False, name="Camera Helper"
        )

    def start(self):
        self.thread.start()
        self.queue.put({"tilt": OPEN})
        self.queue.put({"point": STRAIGHT})

    def shutdown(self):
        self.queue.put({"tilt": CLOSE})
        self.queue.put({"point": STRAIGHT})
        self.queue.put(None)
        self.thread.join()

    def __worker(self):
        while True:
            cmd_opts = self.queue.get()
            if cmd_opts is None:
                break
            self.execute_command(cmd_opts)
            self.queue.task_done()

    def execute_command(self, cmd_opts: cmds):
        if cmd_opts.get("tilt") == CLOSE:
            self.tilt_servo.close_camera()
        elif cmd_opts.get("tilt") == OPEN:
            self.tilt_servo.open_camera()
        elif cmd_opts.get("point") == LEFT:
            self.rotate_servo.point_left()
        elif cmd_opts.get("point") == RIGHT:
            self.rotate_servo.point_right()
        elif cmd_opts.get("point") == STRAIGHT:
            self.rotate_servo.point_straight()
        elif cmd_opts.get("rotate_to_angle"):
            self.rotate_servo.rotate_to_angle(cmd_opts.get("rotate_to_angle"))
        else:
            self.log.error("Invalid command")
