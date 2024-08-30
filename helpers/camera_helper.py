from components.servos.modules.camera_servo import CameraServo as camera_servo
from components.servos.modules.servo_iface import (
    SERVO_ID_ROTATION,
    SERVO_ID_TILT,
)
import logging, threading, queue
from typing import TypedDict, Optional, Dict

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
    def __init__(self):
        self.log = logging.getLogger("bumble")
        self.tilt_ctrl_servo = camera_servo(id=SERVO_ID_TILT)
        self.rotate_servo = camera_servo(id=SERVO_ID_ROTATION)
        self.queue = queue.Queue()
        self.thread = threading.Thread(
            target=self.__worker, daemon=False, name="Camera Helper"
        )
        self.clear_flag = threading.Event()

    def start(self):
        self.thread.start()

    def shutdown(self):
        cmd: cmds = {"tilt": CLOSE, "point": STRAIGHT, "rotate_to_angle": None}
        self.queue.put(cmd)
        self.queue.put(None)
        self.thread.join()

    def post_message(self, cmd_opts: cmds):
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
        if cmd_opts.get("tilt"):
            if cmd_opts.get("tilt") == OPEN:
                self.tilt_servo.open_camera()
            elif cmd_opts.get("tilt") == CLOSE:
                self.tilt_servo.close_camera()

        if cmd_opts.get("point"):
            if cmd_opts.get("point") == LEFT:
                self.rotate_servo.point_left()
            elif cmd_opts.get("point") == RIGHT:
                self.rotate_servo.point_right()
            elif cmd_opts.get("point") == STRAIGHT:
                self.rotate_servo.point_straight()

        if cmd_opts.get("rotate_to_angle"):
            cmd_obj = cmd_opts.get("rotate_to_angle")
            self.rotate_servo.adjust_angle(
                cmd_obj.get("angle"), cmd_obj.get("direction")
            )

        self.clear_flag.set()
