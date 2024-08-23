from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from board import SCL, SDA
import busio
import logging

WIDTH_PX = 128
HEIGHT_PX = 64

logger = logging.getLogger(__name__)


class _TextArea(object):
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class TextAreas(object):
    def __init__(self) -> None:
        self._i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(WIDTH_PX, HEIGHT_PX, self._i2c)
        self.image = Image.new("1", (self.disp.width, self.disp.height))
        self.draw = ImageDraw.Draw(self.image)
        self.area1 = _TextArea(0, 0, 127, 15)
        self.area2 = _TextArea(0, 16, 127, 33)
        self.area3 = _TextArea(0, 31, 127, 48)
        self.area4 = _TextArea(0, 46, 127, 63)
        self.font = ImageFont.truetype("VCR_OSD_MONO_1.001.ttf", 15)

    def setup(self):
        self.disp.fill(0)
        self.disp.show()

    def clearArea1(self):
        self.draw.rectangle(
            (self.area1.left, self.area1.top, self.area1.right, self.area1.bottom),
            outline=0,
            fill=0,
        )
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def clearArea2(self):
        self.draw.rectangle(
            (self.area2.left, self.area2.top, self.area2.right, self.area2.bottom),
            outline=0,
            fill=0,
        )
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def clearArea3(self):
        self.draw.rectangle(
            (self.area3.left, self.area3.top, self.area3.right, self.area3.bottom),
            outline=0,
            fill=0,
        )
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def clearArea4(self):
        self.draw.rectangle(
            (self.area4.left, self.area4.top, self.area4.right, self.area4.bottom),
            outline=0,
            fill=0,
        )
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def writeArea1(self, text):
        logger.debug(f"Writing to area 1: {text}")
        self.clearArea1()
        self.draw.text((self.area1.left, self.area1.top), text, font=self.font, fill=1)
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def writeArea2(self, text):
        logger.debug(f"Writing to area 2: {text}")
        self.clearArea2()
        self.draw.text((self.area2.left, self.area2.top), text, font=self.font, fill=1)
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def writeArea3(self, text):
        logger.debug(f"Writing to area 3: {text}")
        self.clearArea3()
        self.draw.text((self.area3.left, self.area3.top), text, font=self.font, fill=1)
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def writeArea4(self, text):
        logger.debug(f"Writing to area 4: {text}")
        self.clearArea4()
        self.draw.text((self.area4.left, self.area4.top), text, font=self.font, fill=1)
        self.disp.image(self.image)
        # self.disp.display()
        self.disp.show()

    def clear(self):
        # self.disp.clear()
        # self.disp.display()
        self.disp.fill(0)
        self.disp.show()
