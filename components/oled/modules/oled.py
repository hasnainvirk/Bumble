"""
OLED module to display text, images, emojis and usage statistics on OLED screen
"""

import os
import logging
from typing import TypedDict, Optional

import adafruit_ssd1306
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont


# Dimensions for OLED display
WIDTH_PX = 128
HEIGHT_PX = 64

# text constants
AREA_1 = 1
AREA_2 = 2
AREA_3 = 3
AREA_4 = 4

# emoji constants
HAPPY = "happy"
SAD = "sad"
ANGRY = "angry"

# folder name where resources are stored
RESOURCES_FOLDER = "resources"

test_cmd_options = TypedDict(
    "test_cmd_options",
    {
        # run oled command with text on OLED screen
        "text": Optional[bool],
        # run oled command with image on OLED screen
        "image": Optional[str],
        # run oled command with emoji on OLED screen
        "emoji": Optional[str],
        # run oled command with usage states on OLED screen
        "stats": Optional[bool],
    },
)


# private helper class
class TextArea(object):
    """
    Class to define text areas on the OLED display.
    """

    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class Oled:
    """
    Class to interact with the OLED display.
    """

    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(WIDTH_PX, HEIGHT_PX, self.i2c)
        self.resources = RESOURCES_FOLDER
        self.log = logging.getLogger("bumble")
        self.areas = {}
        self.area_list = [AREA_1, AREA_2, AREA_3, AREA_4]
        self.emojis = [HAPPY, SAD, ANGRY]
        self.wipe()
        self.__inialize()

    def __inialize(self):
        self.image = Image.new("1", (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        font_path = os.path.join(
            os.path.dirname(__file__), RESOURCES_FOLDER, "VCR_OSD_MONO_1.001.ttf"
        )
        self.font = ImageFont.truetype(font_path, 15)

    def cleanup(self):
        """
        Clean up the OLED display.
        """
        self.disp.poweroff()
        self.log.critical("Shutting down OLED")
        self.i2c.deinit()

    def create_text_areas(self):
        """
        Create text areas on the OLED display.
        """
        self.areas[AREA_1] = TextArea(0, 0, 127, 15)
        self.areas[AREA_2] = TextArea(0, 16, 127, 33)
        self.areas[AREA_3] = TextArea(0, 31, 127, 48)
        self.areas[AREA_4] = TextArea(0, 46, 127, 63)

    def get_area(self, area_number) -> TextArea | None:
        """
        Get the specified text area on the OLED display.
        """
        if area_number == AREA_1:
            return self.areas.get(AREA_1)
        elif area_number == AREA_2:
            return self.areas.get(AREA_2)
        elif area_number == AREA_3:
            return self.areas.get(AREA_3)
        elif area_number == AREA_4:
            return self.areas.get(AREA_4)
        else:
            return None

    def wipe(self):
        """
        Clear the OLED display.
        """
        self.disp.fill(0)
        self.disp.show()
