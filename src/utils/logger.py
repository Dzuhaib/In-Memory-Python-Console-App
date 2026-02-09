"""Structured logging setup for the todo application."""

import logging
import sys
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        name: Logger name (defaults to root logger)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or "todo")

    # Only configure if no handlers exist
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)

        # Structured format: [LEVEL] [TIMESTAMP] [MODULE] message
        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s [%(module)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Prevent propagation to root logger
        logger.propagate = False

    return logger
