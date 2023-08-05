from unittest import TestCase

from km3astro.random import random_azimuth, random_zenith, random_date


class TestRandom(TestCase):
    def setUp(self):
        self.n_evts = 100
        self.n_evts_funny = 1e2

    def test_zenith(self):
        zen = random_zenith(n=self.n_evts)
        assert zen.shape[0] == self.n_evts
        zen2 = random_zenith(n=self.n_evts_funny)
        self.assertAlmostEqual(zen2.shape[0], self.n_evts_funny)

    def test_azimuth(self):
        azi = random_azimuth(n=self.n_evts_funny)
        assert azi.shape[0] == self.n_evts_funny
        azi2 = random_azimuth(n=self.n_evts_funny)
        self.assertAlmostEqual(azi2.shape[0], self.n_evts_funny)

    def test_date(self):
        tim = random_date(n=self.n_evts)
        assert tim.shape[0] == self.n_evts
        tim2 = random_date(n=self.n_evts_funny)
        self.assertAlmostEqual(tim2.shape[0], self.n_evts_funny)
