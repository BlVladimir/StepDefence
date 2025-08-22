from scripts.main_classes.logging_config import setup_logging
from scripts.main_classes.main_class import StepDefence

setup_logging()

if __name__ == "__main__":
    game = StepDefence()
    game.run()