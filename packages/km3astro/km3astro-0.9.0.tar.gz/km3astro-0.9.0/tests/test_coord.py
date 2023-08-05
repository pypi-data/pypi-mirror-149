from unittest import TestCase

import numpy as np
import pandas as pd

from numpy.testing import assert_allclose
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.time import Time
from astropy.io import ascii
from km3net_testdata import data_path

import km3astro.coord as kc
import km3astro.frame as kf

from km3astro.random import random_date


class TestCoord(TestCase):
    def setUp(self):
        self.n_evts = 100
        self.n_evts_funny = 1e2

    def test_neutrino_flip_degree(self):
        phi = np.array([97.07, 23.46, 97.07, 192.5, 333.33])
        theta = np.array([135.0, 11.97, 22.97, 33.97, 85.23])
        azi_exp = np.array([277.07, 203.46, 277.07, 12.5, 153.33])
        zen_exp = np.array([45.0, 168.03, 157.03, 146.03, 94.77])
        azi, zen = kc.neutrino_to_source_direction(phi, theta, radian=False)
        assert_allclose(azi, azi_exp)
        assert_allclose(zen, zen_exp)

    def test_neutrino_flip_radian(self):
        phi = np.array([97.07, 23.46, 97.07, 192.5, 333.33]) * np.pi / 180
        theta = np.array([135.0, 11.97, 22.97, 33.97, 85.23]) * np.pi / 180
        azi_exp = np.array([277.07, 203.46, 277.07, 12.5, 153.33]) * np.pi / 180
        zen_exp = np.array([45.0, 168.03, 157.03, 146.03, 94.77]) * np.pi / 180
        azi, zen = kc.neutrino_to_source_direction(phi, theta, radian=True)

        assert_allclose(azi, azi_exp)
        assert_allclose(zen, zen_exp)


class TestCoordRandom(TestCase):
    def test_sun(self):
        date = random_date(n=100)
        sun = kc.sun_local(date, loc="orca")


class TestConvergenceAngle(TestCase):
    def test_convergence_angle(self):
        ca = kf.convergence_angle(1.5, 1.3)
        self.assertAlmostEqual(-0.00897440033130838, ca)


class TestUTMStuff(TestCase):
    def test_utm_zone(self):
        assert 38 == kf.utm_zone(np.pi / 180 * 42.8871)

    def test_longitude_of_central_meridian(self):
        self.assertAlmostEqual(0.785398163397448, kf.longitude_of_central_meridian(38))


class TestAntaresBenchmark(TestCase):
    def setUp(self):
        self.tol = 0.01 * u.deg
        self.gal_tol = 0.02 * u.deg

    def test_antares_objects(self):
        # FIXME
        antares_objects_data = ascii.read(
            data_path("astro/antares_astro_objects_benchmark.csv")
        )
        for obj in antares_objects_data:
            time = Time(" ".join([obj["date"], obj["time"]]))

            theta = np.deg2rad(obj["theta"])
            phi = np.deg2rad(obj["phi"])

            # check azimuth and zenith conversion
            azimuth, zenith = kc.neutrino_to_source_direction(phi, theta)
            self.assertAlmostEqual(azimuth[0], np.deg2rad(obj["azimuth"]))
            self.assertAlmostEqual(zenith[0], np.deg2rad(obj["zenith"]))

            event = kc.local_event(phi, time, theta, location="antares")

            equat = event.fk5
            dec = equat.dec
            ra = equat.ra

            ref = SkyCoord(
                " ".join([obj["RA-J2000"], obj["DEC-J2000"]]),
                unit=(u.hourangle, u.deg),
                frame="fk5",
            )

            # from astropy.coordinates import Angle
            # assert np.abs(Angle(obj["DEC-J2000"] + " hours") - event.fk5.dec) < self.tol
            # assert np.abs(obj["RA-J2000"] * u.deg - event.fk5.ra) < self.tol

            # assert np.abs(dec - ref.fk5.dec) < 0.0001 * u.deg
            # assert np.abs(ra - ref.fk5.ra) < 0.0001 * u.deg

    def test_antares_coordinate_system_benchmarks(self):
        antares_objects_data = ascii.read(
            data_path("astro/antares_coordinate_systems_benchmark.csv")
        )
        for obj in antares_objects_data:
            print(obj)
            time = Time(" ".join([obj["date"], obj["time"]]))

            theta = np.deg2rad(obj["theta"])
            phi = np.deg2rad(obj["phi"])

            # check azimuth and zenith conversion
            azimuth, zenith = kc.neutrino_to_source_direction(phi, theta)
            print("azimuth: ", azimuth, np.rad2deg(azimuth))
            print("zenith: ", zenith, np.rad2deg(zenith))
            self.assertAlmostEqual(azimuth[0], np.deg2rad(obj["azimuth"]))
            self.assertAlmostEqual(zenith[0], np.deg2rad(obj["zenith"]))

            event = kc.local_event(phi, time, theta, location="antares")
            print(event.fk5)
            print(event.galactic)

            # ref = SkyCoord(obj["RA-J2000"], obj["DEC-J2000"], unit=u.deg, frame="fk5")

            assert np.abs(obj["DEC-J2000"] * u.deg - event.fk5.dec) < self.tol
            assert np.abs(obj["RA-J2000"] * u.deg - event.fk5.ra) < self.tol

            print(obj["gal_lat"], event.galactic.b.deg[0])
            assert (
                np.abs(obj["gal_lat"] - event.galactic.b.deg[0]) * u.deg < self.gal_tol
            )
            assert (
                np.abs(obj["gal_lon"] - event.galactic.l.deg[0]) * u.deg < self.gal_tol
            )
