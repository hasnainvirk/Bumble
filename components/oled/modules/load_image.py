"""
Load an image file and display it on the OLED.
"""

import os
from PIL import Image as pil_image
from components.oled.modules.oled import Oled


class Image(Oled):
    """
    Class to load an image file and display it on the OLED.
    """

    def load_image(self, img: str):
        """
        Load the specified image file on the OLED display.
        """
        if img:
            image_path = os.path.join(os.path.dirname(__file__), self.resources, img)
        else:
            self.log.error("No image provided.")
            return

        try:
            # Open an image file
            image = pil_image.open(image_path)
        except IOError as e:
            self.log.error("Error opening image file: %s}", e)
            return

        try:
            # Resize the image to fit into 128x64 pixels
            image = image.resize((self.disp.width, self.disp.height))
        except Exception as e:
            self.log.error("Error resizing image: %s", e)
            return

        try:
            # Convert the image to '1' mode (1-bit pixels, black and white)
            image = image.convert("1")
        except Exception as e:
            self.log.error("Error converting image: %s", e)
            return

        try:
            # Display the image on the OLED
            self.disp.image(image)
            self.disp.show()
        except Exception as e:
            self.log.error("Error displaying image: %s", e)
            return
