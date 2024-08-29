from components.wheels.modules.lower_left_wheel import LowerLeftWheel
from components.wheels.modules.lower_right_wheel import LowerRightWheel
from components.wheels.modules.upper_left_wheel import UpperLeftWheel
from components.wheels.modules.upper_right_wheel import UpperRightWheel
from components.ultrasonic_sensor.modules.ultrasonic_sensor import (
    UltrasonicSensor as ultrasonic_sensor,
)
from components.servos.modules.ultrasonic_sensor_servo import (
    UltrasonicSensorServo as ultrasonic_sensor_servo,
)

import queue, threading, logging, time

from components.wheels.modules.wheel_iface import (
    wheel_ctrl_options,
    WheelIface,
    DIRECTION_BACKWARD,
    DIRECTION_FORWARD,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_NONE,
    UPPER_LEFT_WHEEL,
    LOWER_LEFT_WHEEL,
    UPPER_RIGHT_WHEEL,
    LOWER_RIGHT_WHEEL,
    wheel_msg_action,
    wheel_message,
)


class DriveSystem:
    def __init__(self, speed=50):
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
        self.__wheel: WheelIface = None
        self.__speed = speed
        self.__is_driving = False
        for wheel in self.__wheels:
            self.__wheel = self.__ctrl.get(wheel)
            self.__wheel.set_speed(self.__speed)
        self.__queue = queue.Queue()
        self.__threads = []
        self.log = logging.getLogger("bumble")
        self.__stop_flag = threading.Event()
        self.__safety_flag = threading.Event()
        self.__driving_status_lock = threading.Lock()
        self.__safety_distance_lock = threading.Lock()
        self.__drive_train_work_done_lock = threading.Lock()
        self.__drive_train_worker_work_done_status: dict = {
            UPPER_LEFT_WHEEL: False,
            LOWER_LEFT_WHEEL: False,
            UPPER_RIGHT_WHEEL: False,
            LOWER_RIGHT_WHEEL: False,
        }

        self.__sensor = ultrasonic_sensor()
        self.__servo = ultrasonic_sensor_servo()

    def start(self):
        self.__start_drive_train_workers()
        self.__start_collision_detection_worker()

    def shutdown(self):
        # Stop all threads by sending None to the queue
        for _ in self.__wheels:
            self.__queue.put(None)
        self.__stop_flag.set()

        for thread in self.__threads:
            thread.join()

    def post_message(
        self,
        direction: str,
        slow_down: bool = False,
        delay: float = None,
        step: int = None,
    ):
        if direction == DIRECTION_FORWARD:
            upper_left_wheel_dir = DIRECTION_FORWARD
            lower_left_wheel_dir = DIRECTION_FORWARD
            upper_right_wheel_dir = DIRECTION_FORWARD
            lower_right_wheel_dir = DIRECTION_FORWARD
        elif direction == DIRECTION_BACKWARD:
            upper_left_wheel_dir = DIRECTION_BACKWARD
            lower_left_wheel_dir = DIRECTION_BACKWARD
            upper_right_wheel_dir = DIRECTION_BACKWARD
            lower_right_wheel_dir = DIRECTION_BACKWARD
        elif direction == DIRECTION_LEFT:
            upper_left_wheel_dir = DIRECTION_BACKWARD
            lower_left_wheel_dir = DIRECTION_BACKWARD
            upper_right_wheel_dir = DIRECTION_FORWARD
            lower_right_wheel_dir = DIRECTION_FORWARD
        elif direction == DIRECTION_RIGHT:
            upper_left_wheel_dir = DIRECTION_FORWARD
            lower_left_wheel_dir = DIRECTION_FORWARD
            upper_right_wheel_dir = DIRECTION_BACKWARD
            lower_right_wheel_dir = DIRECTION_BACKWARD
        else:
            upper_left_wheel_dir = DIRECTION_NONE
            lower_left_wheel_dir = DIRECTION_NONE
            upper_right_wheel_dir = DIRECTION_NONE
            lower_right_wheel_dir = DIRECTION_NONE

        message: wheel_message = {
            UPPER_LEFT_WHEEL: {
                "direction": upper_left_wheel_dir,
                "name": UPPER_LEFT_WHEEL,
                "speed": 0 if upper_left_wheel_dir == DIRECTION_NONE else self.__speed,
                "slow_down": slow_down,
                "delay": delay,
                "step": step,
            },
            LOWER_LEFT_WHEEL: {
                "direction": lower_left_wheel_dir,
                "name": LOWER_LEFT_WHEEL,
                "speed": 0 if lower_left_wheel_dir == DIRECTION_NONE else self.__speed,
                "slow_down": slow_down,
                "delay": delay,
                "step": step,
            },
            UPPER_RIGHT_WHEEL: {
                "direction": upper_right_wheel_dir,
                "name": UPPER_RIGHT_WHEEL,
                "speed": 0 if upper_right_wheel_dir == DIRECTION_NONE else self.__speed,
                "slow_down": slow_down,
                "delay": delay,
                "step": step,
            },
            LOWER_RIGHT_WHEEL: {
                "direction": lower_right_wheel_dir,
                "name": LOWER_RIGHT_WHEEL,
                "speed": 0 if lower_right_wheel_dir == DIRECTION_NONE else self.__speed,
                "slow_down": slow_down,
                "delay": delay,
                "step": step,
            },
        }

        for _ in self.__wheels:
            self.__queue.put(message)
        self.log.debug(f"Message posted: {message}")

    def __start_drive_train_workers(self):
        for wheel in self.__wheels:
            thread = threading.Thread(
                target=self.__drive_train_worker,
                args=(wheel,),
                name=f"Controller Thread for {wheel} wheel",
            )
            thread.daemon = False
            thread.start()
            self.__threads.append(thread)

    def __start_collision_detection_worker(self):
        thread = threading.Thread(
            target=self.__collisions_detection_worker,
            name="Collision dection thread",
        )
        thread.daemon = False
        thread.start()
        self.__threads.append(thread)

    def __set_drive_train_worker_work_done_status(self, wheel_name, status):
        with self.__drive_train_work_done_lock:
            self.__drive_train_worker_work_done_status[wheel_name] = status

    def __get_drive_train_worker_work_done_status(self):
        with self.__drive_train_work_done_lock:
            if all(self.__drive_train_worker_work_done_status.values()):
                return True
            return False

    def __drive_train_worker(self, wheel_name):
        while True:
            self.log.debug(f"Worker for {wheel_name} waiting for message")
            message = self.__queue.get()
            if message is None:
                self.log.debug(f"Stopping {wheel_name} worker ...")
                self.__ctrl[wheel_name].stop()
                self.__set_driving_status(False)
                self.__safety_flag.set()
                break
            action: wheel_msg_action = message.get(wheel_name)
            self.log.debug(f"Processing message: {action}")
            self.__ctrl[wheel_name].process_message(action)
            if action.get("direction") != DIRECTION_NONE:
                self.__set_driving_status(True)
            else:
                self.__set_driving_status(False)
            self.__set_drive_train_worker_work_done_status(wheel_name, True)
            self.log.debug(f"{wheel_name} worker done ...")
            self.__queue.task_done()
            if self.__get_drive_train_worker_work_done_status():
                self.__drive_train_worker_work_done_status = {
                    UPPER_LEFT_WHEEL: False,
                    LOWER_LEFT_WHEEL: False,
                    UPPER_RIGHT_WHEEL: False,
                    LOWER_RIGHT_WHEEL: False,
                }
                # unblock the collision detection worker
                self.__safety_flag.set()
                self.log.debug("RELEASING COLLECTION DETECTION WORKER")

    def __collisions_detection_worker(self):
        while not self.__stop_flag.is_set():
            if self.__sensor is not None:
                distance = self.__sensor.get_distance()
                # self.log.debug(f"Distance: {distance} cm")
                if distance < 20:
                    self.log.warning(f"Collision Warning {distance} cm")
                    if self.__get_driving_status():
                        self.post_message(DIRECTION_NONE)
                        self.log.debug("BLOCKING DRIVE TRAIN WORKERS STOP")
                        # wait until car is stopped
                        self.__safety_flag.wait()  # blocks until the safety flag is set
                        self.__safety_flag.clear()
                        self.log.debug("COLLISION DETECTION UNBLOCKED")
                        # Decide which direction to go
                        decision_matrix = self.__get_safe_direction()
                        recommendation = max(decision_matrix, key=decision_matrix.get)
                        self.log.debug(
                            f"Recommendation: {recommendation}, {decision_matrix[recommendation]}cm"
                        )
                        if recommendation == "straight":
                            self.post_message(DIRECTION_FORWARD)
                        elif recommendation == "left":
                            self.post_message(DIRECTION_LEFT)
                        elif recommendation == "right":
                            self.post_message(DIRECTION_RIGHT)

                        # wait until car acts on the recommendation
                        # delay for allowing the turn
                        self.__block_until_safety_flag_set(delay=1)

                        # wait until car stops after turning
                        if recommendation == "left" or recommendation == "right":
                            self.post_message(DIRECTION_NONE)
                            self.__block_until_safety_flag_set()

                        # wait until car starts moving forward
                        self.post_message(DIRECTION_FORWARD)
                        self.__block_until_safety_flag_set()

    def __set_driving_status(self, status: bool):
        with self.__driving_status_lock:
            self.__is_driving = status

    def __get_driving_status(self):
        with self.__driving_status_lock:
            return self.__is_driving

    def __block_until_safety_flag_set(self, delay: int = None):
        self.__safety_flag.wait()
        self.__safety_flag.clear()
        if delay:
            time.sleep(delay)

    def __get_safe_direction(self):
        with self.__safety_distance_lock:
            self.__servo.point_right()
            dist_right: float = self.__sensor.get_distance()
            self.__servo.point_left()
            dist_left: float = self.__sensor.get_distance()
            self.__servo.point_straight()
            dist_straight: float = self.__sensor.get_distance()
            return {"right": dist_right, "left": dist_left, "straight": dist_straight}
