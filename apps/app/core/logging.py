from __future__ import annotations

import logging

from app.core.config import settings
from app.core.constants import LOG_DATE_FORMAT, LOG_FORMAT

_configured = False


def configure_logging(force: bool = False) -> None:
    global _configured
    if _configured and not force:
        return
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    _configured = True


def get_logger(name: str | None = None) -> logging.Logger:
    if not _configured:
        configure_logging()
    return logging.getLogger(name)
