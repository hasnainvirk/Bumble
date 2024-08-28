import socket
import threading
import logging
from components.drive_system.modules.drive_system import DriveSystem as drive_system


class KeyboardDriveControl:

    def __init__(self, host="0.0.0.0", port=5555) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.log = logging.getLogger("bumble")
        self.car_controller = drive_system()
        self.stop_flag = threading.Event()

    def start(self):
        self.thread = threading.Thread(
            target=self.__run, name="Keyboard Controller Server", daemon=False
        )
        self.thread.start()

    def shutdown(self):
        self.stop_flag.set()
        self.thread.join()

    def execute_command(self, command):
        if command == "UP":
            self.car_controller.drive_forward(duration=0.2)
        elif command == "DOWN":
            self.car_controller.drive_backward(duration=0.2)
        elif command == "LEFT":
            self.car_controller.turn_left(duration=0.2)
        elif command == "RIGHT":
            self.car_controller.turn_right(duration=0.2)
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
            except Exception as e:
                self.log.error(f"Error: {e}")
