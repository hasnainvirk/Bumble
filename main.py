import sys, logging, signal, argparse
from colorlog import ColoredFormatter
from helpers.ir_helper import RemoteControlHelper as remote_control
from components.oled.oled_task import OledDisplay as oled
from components.led_panel.led_panel_task import LedPanelTask as led_panel
from helpers.kb_controller_server import UDPControllerServer as udp_controller_server
import RPi.GPIO as GPIO


## Setting up logger
def setup_logger(verbosity: int):
    log_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(len(log_levels) - 1, verbosity)]

    LOGFORMAT = " %(log_color)s%(levelname)-8s%(reset)s | %(filename)s | %(log_color)s%(message)s%(reset)s"
    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    file_h = logging.FileHandler("bumble.log")
    stream.setLevel(log_level)
    file_h.setLevel(log_level)
    stream.setFormatter(formatter)
    file_h.setFormatter(formatter)
    log = logging.getLogger("bumble")
    log.addHandler(stream)
    log.addHandler(file_h)
    log.setLevel(log_level)

    return log


# Argument parser setup
parser = argparse.ArgumentParser(description="Bumble Robot")
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase verbosity level (use -v, -vv, -vvv, etc.)",
)
parser.add_argument(
    "-w",
    "--w",
    type=str,
    help="Choos input method (ir = remote or kb = keyboard)",
)
args = parser.parse_args()

# Setting up logger
log = setup_logger(args.verbose)

if args.w not in ["ir", "kb"]:
    log.error("Invalid input method. Use either 'ir' or 'kb'")
    sys.exit(1)

if args.w == "ir":
    log.info("Starting in IR mode")
    controller = remote_control()
elif args.w == "kb":
    log.info("Starting in KEYBOARD mode")
    controller = udp_controller_server()

oled = oled()
led_panel = led_panel()


def signal_handler(sig, frame):
    log.info("Exit signal received. Exiting...")
    controller.shutdown()
    oled.shutdown()
    led_panel.shutdown()

    GPIO.cleanup()

    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":

    # START OLED
    oled.start()
    # START LED PANEL
    led_panel.start()
    # START INPUT CONTROLLER
    controller.start()

    # wait for exit signal
    signal.pause()
