import os
from PIL import Image
from component_testing.oled.modules.oled import Oled


class LoadImage(Oled):
    def __init__(self) -> None:
        super().__init__()

    def load_image(self, img: str):
        if img:
            self.image_path = os.path.join(
                os.path.dirname(__file__), self.resources, img
            )
        else:
            self.log.error("No image provided.")
            return

        try:
            # Open an image file
            image = Image.open(self.image_path)
        except IOError as e:
            self.log.error(f"Error opening image file: {e}")
            return

        try:
            # Resize the image to fit into 128x64 pixels
            image = image.resize((self.disp.width, self.disp.height))
        except Exception as e:
            self.log.error(f"Error resizing image: {e}")
            return

        try:
            # Convert the image to '1' mode (1-bit pixels, black and white)
            image = image.convert("1")
        except Exception as e:
            self.log.error(f"Error converting image: {e}")
            return

        try:
            # Display the image on the OLED
            self.disp.image(image)
            self.disp.show()
        except Exception as e:
            self.log.error(f"Error displaying image: {e}")
            return
