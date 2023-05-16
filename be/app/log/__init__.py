import logging
import sys
from app import settings
from colorama import init, Fore, Back


__all__ = ["setup_logging"]

init(autoreset=True)


class ColorFormatter(logging.Formatter):
    # Change this dictionary to suit your coloring needs!
    COLORS = {
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED + Back.WHITE,
        "DEBUG": Fore.BLUE,
        "INFO": Fore.GREEN,
        "CRITICAL": Fore.RED + Back.WHITE,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        if color:
            record.name = color + record.name
            record.levelname = color + record.levelname
            record.msg = color + record.msg
        return logging.Formatter.format(self, record)


class ColorLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name, settings.log.LEVEL)
        color_formatter = ColorFormatter(settings.log.FORMAT)
        console = logging.StreamHandler(
            sys.stdout if settings.log.STDOUT else sys.stderr
        )
        console.setFormatter(color_formatter)
        self.addHandler(console)


def setup_logging():
    logging.setLoggerClass(ColorLogger)
