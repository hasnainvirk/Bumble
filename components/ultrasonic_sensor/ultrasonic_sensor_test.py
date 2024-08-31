"""
Ultrasonic Sensor Test Module
"""

import logging
from components.ultrasonic_sensor.modules.ultrasonic_sensor import UltrasonicSensor


class UltrasonicSensorTest:
    """
    Class to test the ultrasonic sensor module
    """

    def __init__(self):
        self.__sensor = UltrasonicSensor()
        self.log = logging.getLogger("bumble")

    def execute_command(self):
        """
        Executes the command to measure the distance using the ultrasonic sensor
        """

        try:
            while True:
                distance = self.__sensor.get_distance()
                self.log.debug(
                    "Measured Distance @ UltrasonicSensorTest = %.2f cm", distance
                )
        except KeyboardInterrupt:
            self.log.debug("Measurement stopped by User")
            self.__sensor.cleanup()
