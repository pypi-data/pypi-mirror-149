import logging
import os
from pathlib import Path
from typing import Union


def get_seed() -> Union[int, None]:
    seed = os.environ.get("PYHARD_SEED")
    if seed is None:
        return seed
    else:
        try:
            return int(seed)
        except ValueError:
            return None


class ColorFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] %(asctime)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter_ = logging.Formatter(log_fmt)
        return formatter_.format(record)


log_file = Path(__file__).parents[2] / "graphene.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

nh = logging.NullHandler()

# formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")  # - %(name)s
formatter = ColorFormatter()

nh.setFormatter(formatter)

logger.addHandler(nh)
