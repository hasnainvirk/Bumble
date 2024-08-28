import redis
import logging
import threading
from components.ultrasonic_sensor.modules.ultrasonic_sensor import (
    UltrasonicSensor as ultrasonic_sensor,
)
from components.servos.modules.ultrasonic_sensor_servo import (
    UltrasonicSensorServo as ultrasonic_sensor_servo,
)


class UltrasonicHelper:
    def __init__(self):
        self.sensor = ultrasonic_sensor()
        self.servo = ultrasonic_sensor_servo()
        self.log = logging.getLogger("bumble")
        self.redis = redis.Redis(host="localhost", port=6379, db=0)

    def get_distance(self) -> float:
        return self.sensor.get_distance()

    def scan_environment(self):
        scan_data = {}
        self.servo.point_right()
        for angle in range(1, 180):
            self.servo.rotate_to(angle)
            distance = self.get_distance()
            self.log.debug(f"Angle: {angle}, Distance: {distance}")
            scan_data[angle] = distance
            self.redis.hset("scan_data", angle, distance)
        self.servo.point_straight()
        return scan_data

    def get_optimal_angle(self):
        scan_data = self.redis.hgetall("scan_data")
        if not scan_data:
            return None
        # Convert scan_data keys and values to integers
        scan_data = {int(k): float(v) for k, v in scan_data.items()}
        # Find the angle with the maximum distance
        optimal_angle = max(scan_data, key=scan_data.get)
        return optimal_angle

    def avoid_obstacles(self):
        scan_data = self.scan_environment()
        optimal_angle = self.get_optimal_angle()
        self.log.debug(f"Optimal Angle: {optimal_angle}")
        self.log.debug(f"Distance: {scan_data[optimal_angle]}")
        self.servo.rotate_to(optimal_angle)

    def decide_direction(self):
        self.servo.point_right()
        dist_right = self.get_distance()
        self.servo.point_left()
        dist_left = self.get_distance()
        self.servo.point_straight()
        dist_straight = self.get_distance()
        return {"right": dist_right, "left": dist_left, "straight": dist_straight}

    def cleanup(self):
        self.sensor.cleanup()
        self.servo.cleanup()
