"""Session descriptor persisted to %APPDATA%/RRT/sessions/."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Session:
    session_id: str
    started_at: datetime
    ended_at: datetime | None = None
    route_name: str = ""
    notes: str = ""
    tags: list[str] = field(default_factory=list)
    rrt_version: str = "0.9.3"

    def duration_s(self) -> float:
        if not self.ended_at:
            return 0.0
        return (self.ended_at - self.started_at).total_seconds()