import logging
import sys
import click
from colorlog import ColoredFormatter
from component_testing.oled.oled_test import OledTest as oled_test
from component_testing.oled.modules.oled import test_cmd_options


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
@click.option("-v", count=True, help="Verbosity level default=error, v=info, vv=debug")
def oled(text, image, emoji, v):
    set_verbosity_level(v) if v else None
    log.info("Running OLED test")
    cmd = oled_test()
    cmd_opts = test_cmd_options(text=text, image=image, emoji=emoji)
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
