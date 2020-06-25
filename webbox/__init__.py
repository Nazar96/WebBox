import logging
import sys


def get_console_logger():
    console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setFormatter(()
    return console_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_logger())
    return logger


webbox_logger = get_logger('webbox')
