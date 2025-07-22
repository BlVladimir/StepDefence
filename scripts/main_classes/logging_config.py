import logging


class ANSIColorFormatter(logging.Formatter):
    """Форматтер с ANSI-цветами для терминала"""

    WHITE = '\033[97m'
    GREY = '\033[37m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

    def format(self, record):

        color = self.WHITE
        if record.levelno >= logging.CRITICAL:
            color = self.RED
        elif record.levelno >= logging.ERROR:
            color = self.RED
        elif record.levelno >= logging.WARNING:
            color = self.YELLOW
        elif record.levelno <= logging.DEBUG:
            color = self.GREY

        message = super().format(record)
        return f"{color}{message}{self.RESET}"

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Консольный обработчик
    console = logging.StreamHandler()
    console.setFormatter(ANSIColorFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(console)