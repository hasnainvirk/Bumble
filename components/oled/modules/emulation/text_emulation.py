"""
This script demonstrates how to emulate drawing text on an OLED display using the Pillow library.
"""

import os
from PIL import Image, ImageDraw, ImageFont


# Constants
WIDTH_PX = 128
HEIGHT_PX = 64
FONT_SIZE = 15
RESOURCES_FOLDER = "resources"
CUR_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(CUR_PATH)


# Create a new image with mode '1' for 1-bit pixels (black and white)
image = Image.new("1", (WIDTH_PX, HEIGHT_PX), 1)  # 1 for white background

# Create a drawing object
draw = ImageDraw.Draw(image)

# Draw a rectangle to represent the OLED display boundaries
draw.rectangle([(0, 0), (WIDTH_PX - 1, HEIGHT_PX - 1)], outline=0, fill=1)

# Load a font
font_path = os.path.join(ROOT_PATH, RESOURCES_FOLDER, "VCR_OSD_MONO_1.001.ttf")
font = ImageFont.truetype(font_path, FONT_SIZE)

# Define the text to draw
TEXT = "Hello, OLED 12"

# Calculate text size and position using textbbox
text_bbox = draw.textbbox((0, 0), TEXT, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# Check if text fits within the display dimensions
fits_horizontally = text_width <= WIDTH_PX
fits_vertically = text_height <= HEIGHT_PX

print(f"Text fits horizontally: {fits_horizontally}")
print(f"Text fits vertically: {fits_vertically}")

# Center the text if it fits
if fits_horizontally and fits_vertically:
    text_x = (WIDTH_PX - text_width) // 2  # Center horizontally
    text_y = (HEIGHT_PX - text_height) // 2  # Center vertically
    draw.text((text_x, text_y), TEXT, font=font, fill=0)  # 0 for black text

# Display the image
image.show()
