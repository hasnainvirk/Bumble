from oled import Oled


class TextAreas(Oled):
    def __init__(self) -> None:
        super().__init__()
        self.create_text_areas()

    def clear_area(self, area_number: int):
        if area_number not in self.areas:
            self.log.error(f"Invalid area number: {area_number}")
            return

        area = self.get_area(area_number)
        self.draw.rectangle(
            (area.left, area.top, area.right, area.bottom),
            outline=0,
            fill=0,
        )
        self.disp.image(self.image)
        self.disp.show()

    def write_area(self, text, area_number: int):
        if area_number not in self.areas:
            self.log.error(f"Invalid area number: {area_number}")
            return

        self.log.debug(f"Writing to area {area_number}: {text}")
        area = self.get_area(area_number)
        self.clear_area(area_number=area_number)
        self.draw.text((area.left, area.top), text, font=self.font, fill=1)
        self.disp.image(self.image)
        self.disp.show()

    def wipe(self):
        self.disp.fill(0)
        self.disp.show()
