import RPi.GPIO as GPIO
import time, logging


class UltrasonicSensor:
    def __init__(self):
        self.__gpio_pins = {
            "trigger": 14,
            "echo": 4,
        }  # GPIO_TRIGGER = 14, GPIO_ECHO = 4
        self.__setup()
        self.logger = logging.getLogger("bumble")

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
        self.log.debug(
            "Measured Distance @ Sensor = {:.2f} cm".format(measured_distance)
        )  # {:.2f},Keep two decimal places
        time.sleep(0.01)
        return measured_distance

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_pins["trigger"], GPIO.OUT)
        GPIO.setup(self.__gpio_pins["echo"], GPIO.IN)

    def __cleanup(self):
        GPIO.cleanup()
