"""
Ultrasonic Sensor Servo Module
"""

from components.servos.modules.servo_iface import ServoIface

GPIO_5 = 5


class UltrasonicSensorServo(ServoIface):
    """
    Ultrasonic Sensor Servo class
    """

    def __init__(self):
        """
        Initializes the Ultrasonic Sensor Servo
        """
        super().__init__(gpio_pin=GPIO_5, name="Ultrasonic Sensor Servo")
        super().point_straight()
