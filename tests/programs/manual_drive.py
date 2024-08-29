import sys, logging, signal
from helpers.ir_helper import RemoteControlHelper as remote_control
from components.oled.oled_task import OledDisplay as oled
from components.led_panel.led_panel_task import LedPanelTask as led_panel
from helpers.kb_controller_server import (
    KeyboardControllerServer as kb_controller_server,
)
from helpers.camera_helper import CameraHelper as camera_helper
from typing import TypedDict, Optional
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

manual_drive_cmd_options = TypedDict(
    "manual_drive_cmd_options",
    {
        "t": Optional[str],
    },
)


class ManualDrive:

    def __init__(self, mode: manual_drive_cmd_options) -> None:
        self.log = logging.getLogger("bumble")
        self.log.debug(f"Mode: {mode.get('t')}")
        self.controller = None
        if mode.get("t") == "ir":
            self.log.info("Starting in IR mode")
            self.controller = remote_control()
        elif mode.get("t") == "kb":
            self.log.info("Starting in KEYBOARD mode")
            self.controller = kb_controller_server()

        self.oled = oled()
        self.led_panel = led_panel()
        self.camera = camera_helper()

        # Register the signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.log.info("Exit signal received. Exiting...")
        if self.controller:
            self.controller.shutdown()
        self.oled.shutdown()
        self.led_panel.shutdown()
        self.camera.shutdown()

        # GPIO.cleanup()

        sys.exit(0)

    def start(self):
        # START INPUT CONTROLLER
        if self.controller:
            self.controller.start()
        # START OLED
        self.oled.start()
        # START LED PANEL
        self.led_panel.start()
        # start the camera
        self.camera.start()

        # wait for exit signal
        signal.pause()
