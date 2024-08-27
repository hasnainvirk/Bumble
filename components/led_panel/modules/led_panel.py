import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)


class LedPanel:
    def __init__(self):
        self.__gpio_pins = {
            "SCLK": 8,
            "DIO": 9,
        }  # GPIO_8 Serial Clock, GPIO_9 Data Input/Output
        self.__setup()

    def display(self, matrix_value):
        try:
            self.__startup_sequence()
            self.__send_data(0xC0)
            for i in range(0, 16):
                self.__send_data(matrix_value[i])
            self.__end_sequence()
            self.__startup_sequence()
            self.__send_data(0x8A)
            self.__end_sequence()
        except Exception as e:
            self.log.error(f"Error: {e}")

    def clear(self):
        try:
            GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.LOW)
            self.__noop()
            GPIO.output(self.__gpio_pins.get("DIO"), GPIO.LOW)
            self.__noop()
            GPIO.output(self.__gpio_pins.get("DIO"), GPIO.LOW)
            self.__noop()
        except Exception as e:
            self.log.error(f"Error: {e}")

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_pins.get("SCLK"), GPIO.OUT)
        GPIO.setup(self.__gpio_pins.get("DIO"), GPIO.OUT)

    def __noop(self):
        time.sleep(0.00003)

    def __startup_sequence(self):
        GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.LOW)
        self.__noop()
        GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.HIGH)
        self.__noop()
        GPIO.output(self.__gpio_pins.get("DIO"), GPIO.HIGH)
        self.__noop()
        GPIO.output(self.__gpio_pins.get("DIO"), GPIO.LOW)
        self.__noop()

    def __send_data(self, data):
        for i in range(0, 8):
            GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.LOW)
            self.__noop()
            if data & 0x01:
                GPIO.output(self.__gpio_pins.get("DIO"), GPIO.HIGH)
            else:
                GPIO.output(self.__gpio_pins.get("DIO"), GPIO.LOW)
            self.__noop()
            GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.HIGH)
            self.__noop()
            data >>= 1
            GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.LOW)

    def __end_sequence(self):
        GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.LOW)
        self.__noop()
        GPIO.output(self.__gpio_pins.get("DIO"), GPIO.LOW)
        self.__noop()
        GPIO.output(self.__gpio_pins.get("SCLK"), GPIO.HIGH)
        self.__noop()
