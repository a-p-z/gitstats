import logging

NAME_COLOR = {
    "git": "\x1b[36m",  # cyan
    "data": "\x1b[96m",  # bright cyan
    "stats": "\x1b[94m",  # bright blue
    "templates": "\x1b[34m",  # blue
}
LEVEL_COLOR = {
    logging.DEBUG: "\x1b[95m",  # bright magenta
    logging.INFO: "\x1b[94m",  # bright blue
    logging.WARNING: "\x1b[93m",  # bright yellow
    logging.ERROR: "\x1b[91m",  # bright red
    logging.CRITICAL: "\x1b[91m",  # bright red
}
RESET = "\x1b[0m"
