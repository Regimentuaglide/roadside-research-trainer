"""Loguru-backed logger factory writing to %APPDATA%/RRT/logs/session.log."""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from rrt.utils.paths import app_data_dir

_configured = False


def _configure() -> None:
    global _configured
    if _configured:
        return
    log_dir = app_data_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        log_dir / "session.log",
        rotation="5 MB",
        retention=5,
        level="DEBUG",
        enqueue=True,
    )
    _configured = True


def get_logger(name: str):
    _configure()
    return logger.bind(module=name)