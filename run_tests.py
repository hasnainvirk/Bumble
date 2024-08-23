import logging
from logging_config import setup_logging
from ComponentTesting.oled.oled_test import OledTestTextAreas

setup_logging()

logger = logging.getLogger(__name__)


def main():
    logger.info("Application started")
    # Your application code here
    OledTestTextAreas.test_text_areas()
    logger.info("Application finished")


if __name__ == "__main__":
    main()
