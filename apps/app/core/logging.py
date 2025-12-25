from __future__ import annotations

import logging
from logging.config import dictConfig


def configure_logging(app_name: str, log_level: str = "INFO") -> logging.Logger:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": log_level.upper(),
            },
        }
    )
    return logging.getLogger(app_name)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
