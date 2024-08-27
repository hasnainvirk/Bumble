import sys, logging, signal, argparse
from colorlog import ColoredFormatter
from helpers.ir_helper import RemoteControlHelper as remote_control


## Setting up logger
def setup_logger(verbosity: int):
    log_levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = log_levels[min(len(log_levels) - 1, verbosity)]

    LOGFORMAT = " %(log_color)s%(levelname)-8s%(reset)s | %(filename)s | %(log_color)s%(message)s%(reset)s"
    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)
    log = logging.getLogger("bumble")
    log.setLevel(log_level)
    log.addHandler(stream)
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
args = parser.parse_args()

# Setting up logger
log = setup_logger(args.verbose)

ir = remote_control()


def signal_handler(sig, frame):
    log.info("Exit signal received. Exiting...")
    ir.shutdown()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    # START REMOTE CONTROL
    ir.start()

    # wait for exit signal
    signal.pause()
