import logging
import sys
import click
from colorlog import ColoredFormatter
from components.oled.oled_test import OledTest as oled_test
from components.wheels.wheels_test import WheelsTest as wheel_test, wheel_cmd_options
from components.drive_system.drive_system_test import (
    DriveSystemTest as drive_test,
    drive_system_cmd_options,
)
from components.oled.modules.oled import test_cmd_options
from components.wheels.modules.wheel_iface import (
    UPPER_LEFT_WHEEL,
    UPPER_RIGHT_WHEEL,
    LOWER_LEFT_WHEEL,
    LOWER_RIGHT_WHEEL,
)

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


@cli.command("oled")
@click.option(
    "-text",
    is_flag=True,
    help="Loads text on the OLED screen",
)
@click.option(
    "-image",
    help="Loads an image on OLED screen. The image should be in resources folder, e.g. $bumble oled --image grumpy_cat.jpg",
)
@click.option(
    "-emoji",
    type=click.Choice(["happy", "sad", "angry"], case_sensitive=False),
    help="Loads an emoji the OLED screen, e.g. $bumble oled --emoji happy",
)
@click.option(
    "-stats",
    is_flag=True,
    help="Loads usage states on the OLED screen",
)
@click.option("-v", count=True, help="Verbosity level default=error, v=info, vv=debug")
def oled(text, image, emoji, stats, v):
    set_verbosity_level(v) if v else None
    log.info("Running OLED test")
    cmd = oled_test()
    cmd_opts = test_cmd_options(text=text, image=image, emoji=emoji, stats=stats)
    cmd.execute_command(cmd_opts=cmd_opts)


@cli.command("wheel")
@click.option(
    "-forward",
    type=click.Choice(
        [UPPER_LEFT_WHEEL, LOWER_LEFT_WHEEL, UPPER_RIGHT_WHEEL, LOWER_RIGHT_WHEEL],
        case_sensitive=False,
    ),
    help="Moves the given wheel forward",
)
@click.option(
    "-backward",
    type=click.Choice(
        [UPPER_LEFT_WHEEL, LOWER_LEFT_WHEEL, UPPER_RIGHT_WHEEL, LOWER_RIGHT_WHEEL],
        case_sensitive=False,
    ),
    help="Moves the given wheel backward",
)
@click.option("-v", count=True, help="Verbosity level default=error, v=info, vv=debug")
def wheel(forward, backward, v):
    set_verbosity_level(v) if v else None
    log.info("Running Wheel test")
    cmd_opts = wheel_cmd_options(forward=forward, backward=backward)
    cmd = wheel_test()
    cmd.execute_command(cmd_opts=cmd_opts)


@cli.command("drive")
@click.option(
    "-forward",
    is_flag=True,
    help="Drive system drives robot  forward",
)
@click.option(
    "-backward",
    is_flag=True,
    help="Drive system drives robot backward",
)
@click.option(
    "-left",
    is_flag=True,
    help="Drive system turns robot left",
)
@click.option(
    "-right",
    is_flag=True,
    help="Drive system turns robot right",
)
@click.option("-v", count=True, help="Verbosity level default=error, v=info, vv=debug")
def drive(forward, backward, left, right, v):
    set_verbosity_level(v) if v else None
    log.info("Running Drive System test")
    cmd = drive_test()
    cmd_opts = drive_system_cmd_options(
        forward=forward, backward=backward, left=left, right=right
    )
    cmd.execute_command(cmd_opts=cmd_opts)


def print_help_and_exit(command: click.command):
    """
    Prints help for the given command and exits.

    Args:
        command (click.command): 'test' command handle
    """
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))
        sys.exit()
