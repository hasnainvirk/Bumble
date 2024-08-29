import socket
import threading
import logging
from components.drive_system.modules.drive_system import DriveSystem as drive_system


class KeyboardDriveControl:

    def __init__(self, host="0.0.0.0", port=5555) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        self.sock.bind((self.host, self.port))
        self.log = logging.getLogger("bumble")
        self.car_controller = drive_system(speed=30, embedded_ultrasonic_sensor=True)
        self.stop_flag = threading.Event()

    def start(self):
        self.car_controller.start()
        self.thread = threading.Thread(
            target=self.__run, name="Keyboard Controller Server", daemon=False
        )
        self.thread.start()

    def shutdown(self):
        self.stop_flag.set()
        try:
            self.sock.close()
        except Exception as e:
            self.log.error(f"Error closing socket: {e}")
        self.car_controller.shutdown()
        self.thread.join()

    def execute_command(self, command):
        if command == "UP":
            self.car_controller.post_message(
                "forward", slow_down=False, delay=0.1, step=0.1
            )
        elif command == "DOWN":
            self.car_controller.post_message(
                "backward", slow_down=False, delay=0.1, step=0.1
            )

        elif command == "LEFT":
            self.car_controller.post_message("left", slow_down=False, delay=0.1, step=5)

        elif command == "RIGHT":
            self.car_controller.post_message(
                "right", slow_down=False, delay=0.1, step=5
            )
        elif command == "STOP":
            self.car_controller.post_message("none", slow_down=True, delay=0.1, step=5)
        else:
            self.log.error(f"Invalid command: {command}")

    def __run(self):
        self.log.info(
            f"Keyboard Controller Server Listening on {self.host}:{self.port}"
        )
        while not self.stop_flag.is_set():
            try:
                data, addr = self.sock.recvfrom(1024)
                command = data.decode("utf-8")
                self.log.debug(f"Received command: {command} from {addr}")
                self.execute_command(command)
            except socket.timeout:
                continue
            except socket.error as e:
                if self.stop_flag.is_set():
                    break
                self.log.error(f"Socket error: {e}")
            except Exception as e:
                self.log.error(f"Error: {e}")
