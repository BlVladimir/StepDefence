from logging import getLogger

from scripts.main_classes.logging_config import setup_logging
from scripts.main_classes.main_class import StepDefence

setup_logging()
logger = getLogger(__name__)

if __name__ == "__main__":
    game = StepDefence()
    game.run()