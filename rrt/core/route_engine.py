"""Core route engine — maintains roadside waypoints and segment statistics."""
from __future__ import annotations

import time
import math
from dataclasses import dataclass, field

from rrt.models.waypoint import Waypoint
from rrt.models.route import Route
from rrt.utils.geo import haversine_m
from rrt.utils.logging_setup import get_logger

log = get_logger("route_engine")


class RouteEngine:
    """Accumulates waypoints during a research drive and computes route metrics."""

    def __init__(self) -> None:
        self.route = Route(name=f"route-{int(time.time())}")
        self._last_ts = 0.0

    def start_segment(self, label: str = "segment") -> None:
        self.route.current_segment = label
        self._last_ts = time.monotonic()
        log.info("segment started: %s", label)

    def add_waypoint(self, wp: Waypoint) -> None:
        now = time.monotonic()
        if self.route.waypoints:
            last = self.route.waypoints[-1]
            wp.distance_from_prev_m = haversine_m(
                last.lat, last.lon, wp.lat, wp.lon
            )
            wp.elapsed_s = now - self._last_ts
        self.route.waypoints.append(wp)
        self._last_ts = now
        log.debug("waypoint +%s (total=%d)", wp.label, len(self.route.waypoints))

    def close_segment(self) -> dict:
        stats = self.stats()
        self.route.segments.append({"label": self.route.current_segment, **stats})
        self.route.current_segment = None
        return stats

    def stats(self) -> dict:
        if not self.route.waypoints:
            return {"count": 0, "distance_m": 0.0, "avg_speed_mps": 0.0}
        dist = sum(w.distance_from_prev_m for w in self.route.waypoints)
        elapsed = sum(w.elapsed_s for w in self.route.waypoints) or 1e-6
        return {
            "count": len(self.route.waypoints),
            "distance_m": round(dist, 2),
            "avg_speed_mps": round(dist / elapsed, 3),
        }

    def annotate(self, label: str, tags: list[str] | None = None) -> Waypoint:
        if not self.route.waypoints:
            raise RuntimeError("cannot annotate before first waypoint")
        last = self.route.waypoints[-1]
        wp = Waypoint(
            lat=last.lat,
            lon=last.lon,
            label=label,
            tags=tags or [],
            note=f"annotated from {last.label}",
        )
        self.route.waypoints.append(wp)
        return wp