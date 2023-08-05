from unittest import TestCase

from km3net_testdata import data_path
import km3astro.testing_tools as ktt


class TestAntaresBenchmarks(TestCase):
    def setUp(self):
        self.angle_threshold = 0.02

    def test_antares_objects(self):
        ktt.test_angle_separation(
            data_path("astro/antares_astro_objects_benchmark.csv"), 
            "antares",
            "antares"
        )

    def test_antares_coordinate_system_benchmarks(self):
        ktt.test_angle_separation(
            data_path("astro/antares_coordinate_systems_benchmark.csv"),
            "antares",
            "antares",
        )

class TestARCABenchmarks(TestCase):
    def setUp(self):
        self.angle_threshold = 0.02

    def test_arca_objects(self):
        ktt.test_angle_separation(
            data_path("astro/ARCA_astro_objects_benchmark.csv"), 
            "arca",
            "arca"
        )

    def test_arca_coordinate_system_benchmarks(self):
        ktt.test_angle_separation(
            data_path("astro/ARCA_coordinate_systems_benchmark.csv"),
            "arca",
            "arca"
        )


class TestORCABenchmarks(TestCase):
    def setUp(self):
        self.angle_threshold = 0.02

    def test_orca_objects(self):
        ktt.test_angle_separation(
            data_path("astro/ORCA_astro_objects_benchmark.csv"),
            "orca",
            "orca"
        )

    def test_orca_coordinate_system_benchmarks(self):
        ktt.test_angle_separation(
            data_path("astro/ORCA_coordinate_systems_benchmark.csv"),
            "orca",
            "orca"
        )
