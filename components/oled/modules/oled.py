import os
from typing import TypedDict, Optional
import adafruit_ssd1306
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import logging


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
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class Oled:
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(WIDTH_PX, HEIGHT_PX, self.i2c)
        self.resources = RESOURCES_FOLDER
        self.log = logging.getLogger("bumble")
        self.areas = [AREA_1, AREA_2, AREA_3, AREA_4]
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

    def create_text_areas(self):
        self.area1 = TextArea(0, 0, 127, 15)
        self.area2 = TextArea(0, 16, 127, 33)
        self.area3 = TextArea(0, 31, 127, 48)
        self.area4 = TextArea(0, 46, 127, 63)

    def get_area(self, area_number) -> TextArea | None:
        if area_number == AREA_1:
            return self.area1
        elif area_number == AREA_2:
            return self.area2
        elif area_number == AREA_3:
            return self.area3
        elif area_number == AREA_4:
            return self.area4
        else:
            return None

    def wipe(self):
        self.disp.fill(0)
        self.disp.show()
