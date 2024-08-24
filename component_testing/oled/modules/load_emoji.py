import time
from PIL import Image, ImageDraw
from oled.modules.oled import Oled, HAPPY, SAD, ANGRY, WIDTH_PX, HEIGHT_PX


class Emoji(Oled):
    def __init__(self):
        super().__init__()

    def load_emoji(self, emoji: str):
        if emoji not in self.emojis:
            self.log.error(f"Invalid emoji number: {emoji}")
            return

        if emoji == HAPPY:
            self.__load_happy()
        elif emoji == SAD:
            self.log.error("SAD emoji not implemented yet.")
        elif emoji == ANGRY:
            self.log.error("ANGRY emoji not implemented yet.")

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

    def __load_happy(self):
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

            # Draw the smiley face with eyes open or closed
            self.__draw_happy_emoji(draw, pos, HEIGHT_PX // 2 - 15, eyes_open)

            # Update the display with the new image
            self.disp.image(image)
            self.disp.show()

            # Toggle the eyes state
            eyes_open = not eyes_open

            # Pause briefly before drawing the next frame
            time.sleep(0.5)
