"""Data model for a single roadside research waypoint."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Waypoint:
    lat: float
    lon: float
    label: str = "wp"
    tags: list[str] = field(default_factory=list)
    note: str = ""
    distance_from_prev_m: float = 0.0
    elapsed_s: float = 0.0
    frame_path: str | None = None

    def as_dict(self) -> dict:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "label": self.label,
            "tags": list(self.tags),
            "note": self.note,
            "distance_from_prev_m": self.distance_from_prev_m,
            "elapsed_s": self.elapsed_s,
            "frame_path": self.frame_path,
        }