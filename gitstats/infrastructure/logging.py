import logging

from gitstats.infrastructure import LEVEL_COLOR
from gitstats.infrastructure import NAME_COLOR
from gitstats.infrastructure import RESET


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        level_color = LEVEL_COLOR.get(record.levelno, RESET)
        name_color = NAME_COLOR.get(record.name, RESET)
        format_ = (
            f"%(asctime)s | "
            f"%(threadName)-10s | "
            f"{level_color}%(levelname)-8s{RESET} "
            f"| {name_color}%(name)-9s"
            f"{RESET} | "
            f"%(message)s"
        )
        formatter = logging.Formatter(format_)
        return formatter.format(record)


logger = logging.getLogger("gitstats")
logger.setLevel(logging.INFO)
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(CustomFormatter())
logger.addHandler(stdout_handler)
