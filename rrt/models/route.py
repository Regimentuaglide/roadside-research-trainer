"""Route aggregate used by RouteEngine and ExportService."""
from __future__ import annotations

from dataclasses import dataclass, field

from rrt.models.waypoint import Waypoint


@dataclass
class Route:
    name: str
    waypoints: list[Waypoint] = field(default_factory=list)
    segments: list[dict] = field(default_factory=list)
    current_segment: str | None = None

    def bounds(self) -> tuple[float, float, float, float] | None:
        if not self.waypoints:
            return None
        lats = [w.lat for w in self.waypoints]
        lons = [w.lon for w in self.waypoints]
        return min(lats), min(lons), max(lats), max(lons)