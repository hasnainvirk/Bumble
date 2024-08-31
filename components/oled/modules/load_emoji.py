"""
This module is used to load an emoji on the OLED display.
"""

import time
from PIL import Image, ImageDraw
from components.oled.modules.oled import (
    Oled,
    HAPPY,
    SAD,
    ANGRY,
    WIDTH_PX,
    HEIGHT_PX,
)


class Emoji(Oled):
    """
    Class to load an emoji on the OLED display.
    """

    def load_emoji(self, emoji: str):
        """
        Load the specified emoji on the OLED display.

        Args: emoji (str): The emoji to load on the OLED display. [happy, sad, angry]
        """
        if emoji not in self.emojis:
            self.log.error("Invalid emoji number: %s", emoji)
            return

        self.__render(emoji)

    # Function to draw a smiley face
    def __draw_happy_emoji(self, draw, pos, radius, eyes_open=True):
        # Draw the face
        draw.ellipse(
            (
                pos - radius,
                HEIGHT_PX // 2 - radius,
                pos + radius,
                HEIGHT_PX // 2 + radius,
            ),
            outline=255,
            fill=0,
        )
        # Draw the eyes
        eye_radius = 3
        eye_y = HEIGHT_PX // 2 - 10
        if eyes_open:
            draw.ellipse(
                (
                    pos - 10 - eye_radius,
                    eye_y - eye_radius,
                    pos - 10 + eye_radius,
                    eye_y + eye_radius,
                ),
                outline=255,
                fill=255,
            )
            draw.ellipse(
                (
                    pos + 10 - eye_radius,
                    eye_y - eye_radius,
                    pos + 10 + eye_radius,
                    eye_y + eye_radius,
                ),
                outline=255,
                fill=255,
            )
        else:
            draw.line(
                (pos - 10 - eye_radius, eye_y, pos - 10 + eye_radius, eye_y), fill=255
            )
            draw.line(
                (pos + 10 - eye_radius, eye_y, pos + 10 + eye_radius, eye_y), fill=255
            )
        # Draw the mouth
        draw.arc(
            (pos - 10, HEIGHT_PX // 2, pos + 10, HEIGHT_PX // 2 + 10),
            start=0,
            end=180,
            fill=255,
        )

    def __draw_angry_emoji(self, draw, pos, eyes_open=True):
        eye_radius = 3
        eye_y = HEIGHT_PX // 2 - 10
        if eyes_open:
            draw.polygon(
                [
                    (pos - 10 - eye_radius, eye_y - eye_radius),
                    (pos - 10, eye_y),
                    (pos - 10 + eye_radius, eye_y - eye_radius),
                ],
                outline=255,
                fill=255,
            )
            draw.polygon(
                [
                    (pos + 10 - eye_radius, eye_y - eye_radius),
                    (pos + 10, eye_y),
                    (pos + 10 + eye_radius, eye_y - eye_radius),
                ],
                outline=255,
                fill=255,
            )
        else:
            draw.line(
                (pos - 10 - eye_radius, eye_y, pos - 10 + eye_radius, eye_y), fill=255
            )
            draw.line(
                (pos + 10 - eye_radius, eye_y, pos + 10 + eye_radius, eye_y), fill=255
            )
        # Draw angry mouth
        draw.line(
            [(pos - 15, HEIGHT_PX // 2 + 20), (pos + 15, HEIGHT_PX // 2 + 20)],
            fill=255,
        )

    def __draw_sad_emoji(self, draw, pos, eyes_open=True):
        eye_radius = 3
        eye_y = HEIGHT_PX // 2 - 10
        if eyes_open:
            draw.ellipse(
                (
                    pos - 10 - eye_radius,
                    eye_y - eye_radius,
                    pos - 10 + eye_radius,
                    eye_y + eye_radius,
                ),
                outline=255,
                fill=255,
            )
            draw.ellipse(
                (
                    pos + 10 - eye_radius,
                    eye_y - eye_radius,
                    pos + 10 + eye_radius,
                    eye_y + eye_radius,
                ),
                outline=255,
                fill=255,
            )
        else:
            draw.line(
                (pos - 10 - eye_radius, eye_y, pos - 10 + eye_radius, eye_y), fill=255
            )
            draw.line(
                (pos + 10 - eye_radius, eye_y, pos + 10 + eye_radius, eye_y), fill=255
            )
        # Draw frown
        draw.arc(
            [(pos - 15, HEIGHT_PX // 2 + 10), (pos + 15, HEIGHT_PX // 2 + 30)],
            start=180,
            end=360,
            fill=255,
        )

    def __draw(self, etype, draw, pos, radius, eyes_open=True):
        if etype == HAPPY:
            self.__draw_happy_emoji(draw, pos, radius, eyes_open)
        elif etype == SAD:
            self.__draw_sad_emoji(draw, pos, eyes_open)
        elif etype == ANGRY:
            self.__draw_angry_emoji(draw, pos, eyes_open)

    def __render(self, etype: str):
        # Create a blank image for drawing.
        image = Image.new("1", (WIDTH_PX, HEIGHT_PX))
        # Create a drawing object.
        draw = ImageDraw.Draw(image)
        # Initialize variables
        pos = WIDTH_PX // 2
        eyes_open = True

        while True:
            # Clear image buffer by drawing a black filled box.
            draw.rectangle((0, 0, WIDTH_PX, HEIGHT_PX), outline=0, fill=0)

            # Draw the emoji face with eyes open or closed
            self.__draw(etype, draw, pos, HEIGHT_PX // 2 - 15, eyes_open)

            # Update the display with the new image
            self.disp.image(image)
            self.disp.show()

            # Toggle the eyes state
            eyes_open = not eyes_open

            # Pause briefly before drawing the next frame
            time.sleep(0.5)
