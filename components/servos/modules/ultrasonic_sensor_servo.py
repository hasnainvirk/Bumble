from components.servos.modules.servo_iface import ServoIface

GPIO_5 = 5


class UltrasonicSensorServo(ServoIface):
    def __init__(self):
        super().__init__(gpio_pin=GPIO_5, name="Ultrasonic Sensor Servo")
        super().point_straight()
