import RPi.GPIO as GPIO
import time, logging


class UltrasonicSensor:
    def __init__(self):
        self.log = logging.getLogger("bumble")
        self.__gpio_pins = {
            "trigger": 14,
            "echo": 4,
        }  # GPIO_TRIGGER = 14, GPIO_ECHO = 4

        self.__setup()

    def get_distance(self):
        # 10us is the trigger signal
        GPIO.output(self.__gpio_pins.get("trigger"), GPIO.HIGH)
        time.sleep(0.00001)  # 10us
        GPIO.output(self.__gpio_pins.get("trigger"), GPIO.LOW)
        while not GPIO.input(self.__gpio_pins.get("echo")):
            pass
        t1 = time.time()
        while GPIO.input(self.__gpio_pins.get("echo")):
            pass
        t2 = time.time()
        measured_distance = ((t2 - t1) * 340 / 2) * 100
        time.sleep(0.01)
        return measured_distance

    def cleanup(self):
        try:
            GPIO.cleanup(
                [
                    self.__gpio_pins.get("trigger"),
                    self.__gpio_pins.get("echo"),
                ]
            )
        except Exception as e:
            self.log.error(f"Error cleaning up GPIO: {e}")

    def __setup(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__gpio_pins.get("trigger"), GPIO.OUT)
            GPIO.setup(self.__gpio_pins.get("echo"), GPIO.IN)
        except Exception as e:
            self.log.error(f"Error setting up GPIO: {e}")
            self.cleanup()
