from components.ultrasonic_sensor.modules.ultrasonic_sensor import UltrasonicSensor
import logging


class UltrasonicSensorTest:
    def __init__(self):
        self.__sensor = UltrasonicSensor()
        self.log = logging.getLogger("bumble")

    def command_execute(self):
        try:
            while True:
                distance = self.__sensor.get_distance()
                self.log.debug(
                    "Measured Distance @ UltrasonicSensorTest = {:.2f} cm".format(
                        distance
                    )
                )
        except KeyboardInterrupt:
            self.log.debug("Measurement stopped by User")
            self.__sensor.cleanup()
