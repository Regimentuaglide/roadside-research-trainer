from rrt.utils.geo import haversine_m


def test_haversine_zero():
    assert haversine_m(10, 20, 10, 20) == 0.0


def test_haversine_known_pair():
    d = haversine_m(51.5000, -0.1278, 48.8566, 2.3522)
    assert 330_000 < d < 360_000
</
</parameter>