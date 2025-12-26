import logging
import os

from app.core.constants import LOG_FORMAT, LOG_LEVEL_ENV


def configure_logging() -> None:
    level_name = os.getenv(LOG_LEVEL_ENV, "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format=LOG_FORMAT)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)
