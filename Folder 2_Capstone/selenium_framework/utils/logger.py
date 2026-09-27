
import logging
import os

from utils.config_reader import PROJECT_ROOT


def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured (e.g. imported multiple times) - avoid duplicate handlers
        return logger

    logger.setLevel(logging.INFO)

    log_dir = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "execution.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
