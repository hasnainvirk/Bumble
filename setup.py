from setuptools import setup

setup(
    name="bumble",
    version="0.1.0",
    packages=[
        "tests",
        "components",
        "components.oled",
        "components.oled.modules",
        "components.wheels",
        "components.wheels.modules",
    ],
    entry_points={"console_scripts": ["bumble = tests.bumble:cli"]},
)
