"""
This module is responsible for creating a UDP server that 
listens for commands from the keyboard controller.
"""

import socket
import threading
import logging
from components.drive_system.modules.drive_system import DriveSystem as drive_system
from helpers.camera_helper import CameraHelper as camera_helper


class KeyboardControllerServer:
    """
    Class to create a UDP server that listens for commands from the keyboard controller
    """

    def __init__(self, host="0.0.0.0", port=5555) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        self.sock.bind((self.host, self.port))
        self.log = logging.getLogger("bumble")
        self.car_controller = drive_system(speed=30)
        self.camera = camera_helper()
        self.stop_flag = threading.Event()
        self.thread = None

    def start(self):
        """
        Start the UDP server
        shutdown must be called to stop the server
        """
        self.car_controller.start()
        self.camera.start()
        self.thread = threading.Thread(
            target=self.__worker, name="UDP Controller Server", daemon=False
        )
        self.thread.start()

    def shutdown(self):
        """
        Shutdown the UDP server
        """
        self.stop_flag.set()
        try:
            self.sock.close()
        except Exception as e:
            self.log.error("Error closing socket: %s", e)
        self.car_controller.shutdown()
        self.camera.shutdown()
        self.thread.join()

    def execute_command(self, command):
        """
        Execute the command received from the keyboard controller
        """
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
        elif command == "ROTATE_CAMERA_LEFT":
            self.camera.post_message(
                {
                    "tilt": None,
                    "point": "left",
                    "rotate_to_angle": None,
                }
            )
        elif command == "ROTATE_CAMERA_RIGHT":
            self.camera.post_message(
                {
                    "tilt": None,
                    "point": "right",
                    "rotate_to_angle": None,
                }
            )
        elif command == "ROTATE_CAMERA_STRAIGHT":
            self.camera.post_message(
                {
                    "tilt": None,
                    "point": "straight",
                    "rotate_to_angle": None,
                }
            )
        elif command == "CAMERA_UP_INCREMENTLY":
            self.camera.post_message(
                {
                    "tilt": "upward",
                    "point": None,
                    "rotate_to_angle": {"angle": 10, "direction": "upward"},
                }
            )
        elif command == "CAMERA_DOWN_INCREMENTLY":
            self.camera.post_message(
                {
                    "tilt": "downward",
                    "point": None,
                    "rotate_to_angle": {"angle": 10, "direction": "downward"},
                }
            )
        elif command == "ROTATE_CAMERA_LEFT_INCREMENTLY":
            self.camera.post_message(
                {
                    "tilt": None,
                    "point": None,
                    "rotate_to_angle": {"angle": 10, "direction": "left"},
                }
            )
        elif command == "ROTATE_CAMERA_RIGHT_INCREMENTLY":
            self.camera.post_message(
                {
                    "tilt": None,
                    "point": None,
                    "rotate_to_angle": {"angle": 10, "direction": "right"},
                }
            )
        elif command == "OPEN_CAMERA":
            self.camera.post_message(
                {
                    "tilt": "open",
                    "point": None,
                    "rotate_to_angle": None,
                }
            )
        elif command == "CLOSE_CAMERA":
            self.camera.post_message(
                {
                    "tilt": "close",
                    "point": None,
                    "rotate_to_angle": None,
                }
            )
        else:
            self.log.error("Invalid command: %s", command)

    def __worker(self):
        self.log.info(
            "Keyboard Controller Server Listening on %s : %d",
            self.host,
            self.port,
        )
        while not self.stop_flag.is_set():
            try:
                data, addr = self.sock.recvfrom(1024)
                command = data.decode("utf-8")
                self.log.debug("Received command: %s from %s", command, addr)
                self.execute_command(command)
            except socket.timeout:
                continue
            except socket.error as e:
                if self.stop_flag.is_set():
                    break
                self.log.error("Socket error: %s", e)
            except Exception as e:
                self.log.error("Error: %s", e)
