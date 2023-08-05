from unittest import TestCase

from km3astro.constants import (
    orca_easting,
    orca_northing,
    orca_utm_zone_letter,
    orca_utm_zone_number,
    orca_latitude,
    orca_longitude,
    arca_easting,
    arca_northing,
    arca_utm_zone_letter,
    arca_utm_zone_number,
    arca_latitude,
    arca_longitude,
)

# taken from loi
arca_latitude_naive = 36 + (16 / 60)  # degree
arca_longitude_naive = 16 + (6 / 60)  # degree
arca_lat_delta = 0.3
arca_lon_delta = 0.3

orca_latitude_naive = 42 + (48.05 / 60)  # degree
orca_longitude_naive = 6 + (1.3368 / 60)  # degree
orca_lat_delta = 0.01
orca_lon_delta = 0.01


class TestUTM(TestCase):
    def test_ref_vs_computed(self):
        self.assertAlmostEqual(
            orca_longitude_naive, orca_longitude, delta=orca_lon_delta
        )
        self.assertAlmostEqual(orca_latitude_naive, orca_latitude, delta=orca_lat_delta)
        self.assertAlmostEqual(
            arca_longitude_naive, arca_longitude, delta=arca_lon_delta
        )
        self.assertAlmostEqual(arca_latitude_naive, arca_latitude, delta=arca_lat_delta)
