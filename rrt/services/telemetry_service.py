"""Local telemetry sink — SQLite-backed event log for research sessions."""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from rrt.utils.logging_setup import get_logger

log = get_logger("telemetry")


class TelemetryService:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS events ("
            "ts REAL, kind TEXT, payload TEXT)"
        )
        self._conn.commit()
        self._buffer: list[tuple] = []

    def record(self, kind: str, payload: dict) -> None:
        self._buffer.append((time.time(), kind, json.dumps(payload)))
        if len(self._buffer) >= 32:
            self.flush()

    def flush(self) -> None:
        if not self._buffer:
            return
        self._conn.executemany("INSERT INTO events VALUES (?, ?, ?)", self._buffer)
        self._conn.commit()
        log.debug("flushed %d telemetry events", len(self._buffer))
        self._buffer.clear()

    def close(self) -> None:
        self.flush()
        self._conn.close()