"""Serializes routes to GeoJSON and JSON session bundles."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from rrt.models.route import Route
from rrt.utils.logging_setup import get_logger

log = get_logger("export")


class ExportService:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def export_route(self, route: Route) -> Path:
        ts = route.name or "route"
        raw_path = self.root / f"{ts}.json"
        raw_path.write_text(json.dumps(asdict(route), indent=2), encoding="utf-8")
        geojson = self._to_geojson(route)
        geo_path = self.root / f"{ts}.geojson"
        geo_path.write_text(json.dumps(geojson, indent=2), encoding="utf-8")
        log.info("exported %s (%d waypoints)", geo_path.name, len(route.waypoints))
        return geo_path

    def _to_geojson(self, route: Route) -> dict:
        coords = [[w.lon, w.lat] for w in route.waypoints]
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {
                        "name": route.name,
                        "segment": route.current_segment,
                        "waypoints": len(route.waypoints),
                    },
                }
            ],
        }