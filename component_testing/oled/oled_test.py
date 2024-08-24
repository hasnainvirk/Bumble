from oled.modules import text_areas, load_image, load_emoji
from oled.modules.oled import AREA_1, AREA_2, AREA_3, AREA_4, test_cmd_options


class OledTest(object):
    def __init__(self) -> None:
        self.text = text_areas.TextAreas()
        self.image = load_image.LoadImage()
        self.emoji = load_emoji.LoadEmoji()

    def execute_command(self, cmd_opts: test_cmd_options):
        if cmd_opts.get("text"):
            self.__test_text_areas()
        if cmd_opts.get("image"):
            self.__test_image_load(cmd_opts.get("image"))
        if cmd_opts.get("emoji"):
            self.__test_emoji_load(cmd_opts.get("emoji"))

    def __test_text_areas(self):
        self.text.write_area("Hello, World!", AREA_1)
        self.text.write_area("Area 2", AREA_2)
        self.text.write_area("Area 3", AREA_3)
        self.text.write_area("Area 4!", AREA_4)

    def __test_image_load(self, ctype: str | None):
        self.image.load_image(ctype)

    def __test_emoji_load(self, ctype: str):
        self.emoji.load_emoji(ctype)
