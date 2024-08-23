import logging
import sys
import click
from colorlog import ColoredFormatter
from component_testing.oled.oled_test import OledTestTextAreas as oled_test


## Setting up logger
LOG_LEVEL = logging.ERROR  # default log level
LOGFORMAT = " %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger("bumble")
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


def set_verbosity_level(verbosity: int):
    """
    Sets verbosity level

    Args:
        verbosity (int): 1 to set info level verbosity, 2 or more than 2 for debug level.
    """
    if verbosity == 1:
        stream.setLevel(logging.INFO)
        log.setLevel(logging.INFO)
    elif verbosity >= 2:
        stream.setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)


@click.group(chain=True)
def cli():
    pass


@cli.command("test")
@click.option("-oled", is_flag=True, help="Run the OLED test on the robot")
@click.option("-v", count=True, help="Verbosity level default=error, v=info, vv=debug")
def test(oled: bool, v: int):
    set_verbosity_level(v) if v else None
    if oled:
        test = oled_test()
        test.test_text_areas()
        print(sys.path)
    pass


def print_help_and_exit(command: click.command):
    """
    Prints help for the given command and exits.

    Args:
        command (click.command): 'test' command handle
    """
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))
        sys.exit()
