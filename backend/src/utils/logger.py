"""Structured logging setup."""

import logging
import sys
from typing import Optional

from config import settings


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        name: Logger name (defaults to root logger)

    Returns:
        Configured logger with structured formatting
    """
    logger = logging.getLogger(name or "todo")

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    return logger
