from rrt.core.route_engine import RouteEngine
from rrt.models.waypoint import Waypoint


def test_add_waypoint_accumulates_distance():
    eng = RouteEngine()
    eng.start_segment("t")
    eng.add_waypoint(Waypoint(lat=51.5000, lon=-0.1278, label="a"))
    eng.add_waypoint(Waypoint(lat=51.5010, lon=-0.1278, label="b"))
    stats = eng.stats()
    assert stats["count"] == 2
    assert stats["distance_m"] > 100


def test_close_segment_records_stats():
    eng = RouteEngine()
    eng.start_segment("seg1")
    eng.add_waypoint(Waypoint(lat=0.0, lon=0.0))
    stats = eng.close_segment()
    assert eng.route.segments[0]["label"] == "seg1"
    assert stats["count"] == 1