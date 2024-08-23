from setuptools import setup

setup(
    name="bumble",
    version="0.1.0",
    packages=[
        "tests",
        "component_testing",
        "component_testing.oled",
        "component_testing.oled.modules",
    ],
    entry_points={"console_scripts": ["bumble = tests.bumble:cli"]},
)
