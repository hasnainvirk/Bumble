import RPi.GPIO as GPIO
import logging, time

SCALING_FACTOR = 11
PULSE_WIDTH_MICROSECONDS = 500.0
PWM_CYCLE_MILLSECONDS = 20.0
MIN_PIN_NUMBER = 0
MAX_PIN_NUMBER = 27


class ServoIface:
    def __init__(self, gpio_pin: int) -> None:
        if gpio_pin is None or gpio_pin < MIN_PIN_NUMBER or gpio_pin > MAX_PIN_NUMBER:
            raise ValueError("Invalid GPIO pin")
        self.log = logging.getLogger("bumble")
        self.gpio_pin = gpio_pin
        self.__setup()

    def generate_pulse(self, angle: int):

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

    def cleanup(self):
        GPIO.cleanup()

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setwarnings(False)
