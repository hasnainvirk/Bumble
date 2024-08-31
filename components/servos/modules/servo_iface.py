"""
This module provides an interface for controlling servos. It includes methods for 
generating pulses to rotate the servo to a specific angle, pointing the servo to 
the right, left, or straight, and opening or closing the camera. The interface also 
includes methods for adjusting the angle of the servo and setting the current angle 
of the servo. The interface uses the RPi.GPIO library to control the GPIO pins on the 
Raspberry Pi.
"""

import logging
import time
import threading
import RPi.GPIO as GPIO


# constants
SCALING_FACTOR = 11
PULSE_WIDTH_MICROSECONDS = 500.0
# SCALING_FACTOR = 5.56
# PULSE_WIDTH_MICROSECONDS = 1000.0
PWM_CYCLE_MILLSECONDS = 20.0
MIN_PIN_NUMBER = 0
MAX_PIN_NUMBER = 27

# constants for any rotation servo
POINTING_STRAIGHT_ANGLE = 90
POINTING_RIGHT_ANGLE = 0
POINTING_LEFT_ANGLE = 180

# constants for identifying camera servo types, defaults to none for other servos
SERVO_ID_TILT = 0  # Camera tilt servo ID
SERVO_ID_ROTATION = 1  # Camera rotation servo ID

# constants for camera tilt servo
OPEN_CAMERA_ANGLE = 90
CLOSE_CAMERA_ANGLE = 0


class ServoIface:
    """
    Interface for controlling servos
    """

    def __init__(self, gpio_pin: int, name: str, tid: int = None) -> None:
        if gpio_pin is None or gpio_pin < MIN_PIN_NUMBER or gpio_pin > MAX_PIN_NUMBER:
            raise ValueError("Invalid GPIO pin")
        self.id = tid
        self.log = logging.getLogger("bumble")
        self.gpio_pin = gpio_pin
        self.lock = threading.Lock()
        self.current_angle = None
        self.name = name
        self.__setup()

    def generate_pulse(self, angle: int):
        """
        Generates a pulse of the given angle that makes the servo rotate to that angle.
        angle: int: The angle to rotate the servo to
        """
        with self.lock:
            if angle < 0 or angle > 180:
                raise ValueError("Invalid angle")

            scaled_pulse_width = (
                angle * SCALING_FACTOR
            ) + PULSE_WIDTH_MICROSECONDS  # The scaled pulse width
            hold_time_seconds = scaled_pulse_width / 1000000.0

            GPIO.output(self.gpio_pin, GPIO.HIGH)
            time.sleep(hold_time_seconds)
            GPIO.output(self.gpio_pin, GPIO.LOW)
            cycle_time_seconds = PWM_CYCLE_MILLSECONDS / 1000.0
            time.sleep(cycle_time_seconds - hold_time_seconds)  # The cycle of 20 ms

    def point_straight(self):
        """
        Points the servo straight
        """
        if self.id == SERVO_ID_TILT:
            self.log.warning(
                "Camera Tilt Servo - Cannot point, use open_camera or close_camera"
            )
            return

        self.log.debug("%s - Point straight", self.name)
        if self.current_angle is None:
            self.force_point_straight()
            return

        i = self.current_angle
        while i > POINTING_STRAIGHT_ANGLE:
            self.generate_pulse(i)
            i -= 1
        while i < POINTING_STRAIGHT_ANGLE:
            self.generate_pulse(i)
            i += 1

        self.set_angle(POINTING_STRAIGHT_ANGLE)

    def point_right(self):
        """
        Points the servo to the right
        """
        if self.id == SERVO_ID_TILT:
            self.log.warning("Camera Servo - Cannot point right")
            return

        self.log.debug("%s - Point Right", self.name)
        if self.current_angle is None:
            self.force_point_right()
            return

        i = self.current_angle
        while i > POINTING_RIGHT_ANGLE:
            self.generate_pulse(i)
            i -= 1
        self.set_angle(i)

    def point_left(self):
        """
        Points the servo to the left
        """
        if self.id == SERVO_ID_TILT:
            self.log.warning("Camera Servo - Cannot point straight")
            return

        self.log.debug("%s - Piont Left", self.name)
        if self.current_angle is None:
            self.force_point_left()
            return

        i = self.current_angle
        while i < POINTING_LEFT_ANGLE:
            self.generate_pulse(i)
            i += 1
        self.set_angle(i)

    def adjust_angle(self, angle: int, direction: str):
        """
        Adjusts the angle of the servo to the given angle
        angle: int: The angle to adjust to
        direction: str: The direction to adjust to [right, left, upward, downward]
        [upward, downward] are only for camera tilt servo.
        """
        if self.current_angle is None:
            self.log.error(
                "Current angle is unknown, try pointing to a known direction first, e.g, all the way right"
            )
            return

        # camera tilt servo can only open or close and the orientation is such that the
        # "right", i.e., towards angle 0 is "downwards" and "left", i.e., towards angle 90
        if self.id == SERVO_ID_TILT:
            if direction == "upward":
                direction = "left"
                desired_angle = self.current_angle + angle
            elif direction == "downward":
                direction = "right"
                desired_angle = self.current_angle - angle
            # direction = "left" if direction == "upward" else "right"

            # desired_angle: int = (
            #     self.current_angle - angle
            #     if direction == "right"
            #     else self.current_angle + angle
            # )
            if desired_angle > OPEN_CAMERA_ANGLE or desired_angle < CLOSE_CAMERA_ANGLE:
                self.log.warning(
                    "Invalid angle for Camera Tilt Servo: %s. Will adjust to allowed value",
                    desired_angle,
                )

                if desired_angle > OPEN_CAMERA_ANGLE:
                    desired_angle = OPEN_CAMERA_ANGLE
                else:
                    desired_angle = CLOSE_CAMERA_ANGLE
                # desired_angle = (
                #     OPEN_CAMERA_ANGLE
                #     if desired_angle > OPEN_CAMERA_ANGLE
                #     else CLOSE_CAMERA_ANGLE
                # )
                self.log.warning("Adjusted angle: %s", desired_angle)
        else:
            if direction == "right":
                desired_angle = self.current_angle - angle
            elif direction == "left":
                desired_angle = self.current_angle + angle

            # desired_angle = (
            #     self.current_angle - angle
            #     if direction == "right"
            #     else self.current_angle + angle
            # )
            # sanity check
            if (
                desired_angle > POINTING_LEFT_ANGLE
                or desired_angle < POINTING_RIGHT_ANGLE
            ):
                self.log.warning(
                    "Invalid angle: %s. Will adjust to allowed value", desired_angle
                )
                if desired_angle > POINTING_LEFT_ANGLE:
                    desired_angle = POINTING_LEFT_ANGLE
                else:
                    desired_angle = POINTING_RIGHT_ANGLE
                # desired_angle = (
                #     POINTING_LEFT_ANGLE
                #     if desired_angle > POINTING_LEFT_ANGLE
                #     else POINTING_RIGHT_ANGLE
                # )
                self.log.warning("Adjusted angle: %s", desired_angle)

        self.log.debug(
            "%s - Rotating by %d degrees, current angle %s, desired_angle %s",
            self.name,
            angle,
            self.current_angle,
            desired_angle,
        )

        i = self.current_angle
        while i > desired_angle:
            self.generate_pulse(i)
            i -= 1
        while i < desired_angle:
            self.generate_pulse(i)
            i += 1

        self.set_angle(i)

    def close_camera(self):
        """
        Closes the camera
        """
        if self.id == SERVO_ID_TILT:
            self.log.debug("%s - Closing Camera", self.name)
            if self.current_angle is None:
                self.force_close_camera()

            i = self.current_angle
            while i > CLOSE_CAMERA_ANGLE:
                self.generate_pulse(i)
                i -= 1
            self.set_angle(i)

    def open_camera(self):
        """
        Opens the camera
        """
        if self.id == SERVO_ID_TILT:
            self.log.debug("%s - Opening Camera", self.name)

            if self.current_angle is None:
                self.force_open_camera()
                return

            i = self.current_angle
            while i > OPEN_CAMERA_ANGLE:
                self.generate_pulse(i)
                i -= 1
            while i < OPEN_CAMERA_ANGLE:
                self.generate_pulse(i)
                i += 1

            self.set_angle(OPEN_CAMERA_ANGLE)

    # we will hopefully never need to use this methods
    def force_point_straight(self):
        """
        Forces the servo to point straight. Do not use this method unless necessary.
        """
        self.log.debug("%s - Force Point straight", self.name)
        for _ in range(0, 50):
            self.generate_pulse(POINTING_STRAIGHT_ANGLE)
        self.set_angle(POINTING_STRAIGHT_ANGLE)

    def force_point_right(self):
        """
        Forces the servo to point right. Do not use this method unless necessary.
        """
        self.log.debug("%s - Force Point Right", self.name)
        for _ in range(0, 50):
            self.generate_pulse(POINTING_RIGHT_ANGLE)
        self.set_angle(POINTING_RIGHT_ANGLE)

    def force_point_left(self):
        """
        Forces the servo to point left. Do not use this method unless necessary.
        """
        self.log.debug("%s - Force Point Left", self.name)
        for _ in range(0, 50):
            self.generate_pulse(POINTING_LEFT_ANGLE)
        self.set_angle(POINTING_LEFT_ANGLE)

    def force_close_camera(self):
        """
        Forces the camera to close. Do not use this method unless necessary.
        """
        self.log.debug("%s - Force Close Camera", self.name)
        for _ in range(0, 50):
            self.generate_pulse(CLOSE_CAMERA_ANGLE)
        self.set_angle(CLOSE_CAMERA_ANGLE)

    def force_open_camera(self):
        """
        Forces the camera to open. Do not use this method unless necessary.
        """
        self.log.debug("%s - Force Open Camera", self.name)
        for _ in range(0, 50):
            self.generate_pulse(OPEN_CAMERA_ANGLE)
        self.set_angle(OPEN_CAMERA_ANGLE)

    def cleanup(self):
        """
        Cleans up the GPIO pins
        """
        GPIO.cleanup(self.gpio_pin)

    def set_angle(self, angle):
        """
        Sets the current angle of the servo
        """
        self.current_angle = angle

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setwarnings(False)
