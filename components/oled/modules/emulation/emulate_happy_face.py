"""
This script demonstrates how to emulate drawing a simple smiley face on the OLED display
"""

import time
from PIL import Image, ImageDraw

# Constants
WIDTH_PX = 128
HEIGHT_PX = 64

# Create a blank image for drawing.
image = Image.new("1", (WIDTH_PX, HEIGHT_PX), 1)  # 1 for white background

# Create a drawing object.
draw = ImageDraw.Draw(image)


# Function to draw a smiley face
def draw_smiley(draw_obj, x, y, are_eyes_open=True):
    """
    Draw a smiley face at the specified position.
    """
    # Draw face
    draw_obj.ellipse((x, y, x + 30, y + 30), outline=0, fill=1)
    # Draw eyes
    if are_eyes_open:
        draw_obj.ellipse((x + 8, y + 8, x + 12, y + 12), outline=0, fill=0)
        draw_obj.ellipse((x + 18, y + 8, x + 22, y + 12), outline=0, fill=0)
    else:
        draw_obj.line((x + 8, y + 10, x + 12, y + 10), fill=0)
        draw_obj.line((x + 18, y + 10, x + 22, y + 10), fill=0)
    # Draw mouth
    draw_obj.arc((x + 8, y + 15, x + 22, y + 25), start=0, end=180, fill=0)


# Set animation parameters
BLINK_INTERVAL = 0.5  # Time between blinks
EYES_OPEN = True

# Initial drawing
draw_smiley(draw, WIDTH_PX // 2 - 15, HEIGHT_PX // 2 - 15, EYES_OPEN)
image.show()

# Animate blinking eyes
print("Press Ctrl-C to quit.")
while True:
    # Toggle eyes state
    EYES_OPEN = not EYES_OPEN

    # Clear the eyes area
    draw.rectangle(
        (
            WIDTH_PX // 2 - 15 + 8,
            HEIGHT_PX // 2 - 15 + 8,
            WIDTH_PX // 2 - 15 + 22,
            HEIGHT_PX // 2 - 15 + 12,
        ),
        fill=1,
    )

    # Redraw the smiley face with the new eyes state
    draw_smiley(draw, WIDTH_PX // 2 - 15, HEIGHT_PX // 2 - 15, EYES_OPEN)

    # Save the image to a file
    # image.save("oled_emulation.png")

    # Display the image
    image.show()

    # Pause briefly before the next frame
    time.sleep(BLINK_INTERVAL)
