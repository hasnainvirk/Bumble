from component_testing.oled.modules import text_areas as areas


class OledTestTextAreas(object):
    def __init__(self) -> None:
        pass

    def test_text_areas():
        areas.setup()
        areas.writeArea1("Hello, World!")
        areas.writeArea2("Area 2")
        areas.writeArea3("Area 3")
        areas.writeArea4("Area 4!")
