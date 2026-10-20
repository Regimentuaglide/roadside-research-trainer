"""Waypoint annotation handler bound to F9."""
from __future__ import annotations

import time

from rrt.utils.logging_setup import get_logger

log = get_logger("annotation")


class AnnotationHandler:
    def __init__(self) -> None:
        self._last_mark = 0.0
        self._counter = 0

    def mark_waypoint(self) -> None:
        now = time.monotonic()
        if now - self._last_mark < 0.25:
            return
        self._last_mark = now
        self._counter += 1
        log.info("waypoint #%d marked", self._counter)

    @property
    def count(self) -> int:
        return self._counter