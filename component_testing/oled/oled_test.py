from component_testing.oled.modules import text_areas


class OledTestTextAreas(object):
    def __init__(self) -> None:
        self.areas = text_areas.TextAreas()

    def test_text_areas(self):
        self.areas.setup()
        self.areas.writeArea1("Hello, World!")
        self.areas.writeArea2("Area 2")
        self.areas.writeArea3("Area 3")
        self.areas.writeArea4("Area 4!")
