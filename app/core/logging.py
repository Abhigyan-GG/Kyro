"""
Kyro — Logging Configuration

Structured logging with file + console handlers.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configure and return the root application logger."""

    logger = logging.getLogger("kyro")
    logger.setLevel(getattr(logging, settings.log.LEVEL.upper(), logging.DEBUG))

    # Prevent duplicate handlers on reload
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (rotating)
    log_dir = os.path.dirname(settings.log.FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        settings.log.FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Kyro logging initialised [level=%s]", settings.log.LEVEL)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the kyro namespace."""
    return logging.getLogger(f"kyro.{name}")
