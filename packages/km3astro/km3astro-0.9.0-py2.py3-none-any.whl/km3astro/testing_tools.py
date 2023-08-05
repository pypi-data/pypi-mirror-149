import numpy as np
import pandas as pd

import km3astro.coord as kc


def test_Skycoord_separation(SC_true, SC_check):

    sep = SC_true.separation(SC_check)
    sep_deg = sep.deg
    return sep_deg


def test_benchmark_conversion(table_true, table_check):

    data_ = [table_true["SkyCoord_base"], table_check["SkyCoord_new"]]
    table_ = pd.concat(data_, axis=1)

    sep_table = table_.apply(
        lambda x: test_Skycoord_separation(x.SkyCoord_base, x.SkyCoord_new),
        axis=1,
        result_type="expand",
    )

    return sep_table


def test_angle_separation(file0, detector_="antares", detector_to_="antares"):

    table_read = kc.reader_from_file(file0)

    angle_treshold = 0.02

    if set(["phi", "theta"]).issubset(table_read.columns):

        table_loc_to_utm = kc.transform_to_new_frame(
            table_read, "ParticleFrame", "UTM", detector_, detector_to_
        )
        table_loc_to_eq = kc.transform_to_new_frame(
            table_read, "ParticleFrame", "equatorial", detector_, detector_to_
        )
        table_loc_to_gal = kc.transform_to_new_frame(
            table_read, "ParticleFrame", "galactic", detector_, detector_to_
        )

    if set(["azimuth", "zenith"]).issubset(table_read.columns):

        table_utm_to_loc = kc.transform_to_new_frame(
            table_read, "UTM", "ParticleFrame", detector_, detector_to_
        )
        table_utm_to_eq = kc.transform_to_new_frame(
            table_read, "UTM", "equatorial", detector_, detector_to_
        )
        table_utm_to_gal = kc.transform_to_new_frame(
            table_read, "UTM", "galactic", detector_, detector_to_
        )

    if set(["RA-J2000", "DEC-J2000"]).issubset(table_read.columns):

        table_eq_to_utm = kc.transform_to_new_frame(
            table_read, "equatorial", "UTM", detector_, detector_to_
        )
        table_eq_to_loc = kc.transform_to_new_frame(
            table_read, "equatorial", "ParticleFrame", detector_, detector_to_
        )
        table_eq_to_gal = kc.transform_to_new_frame(
            table_read, "equatorial", "galactic", detector_, detector_to_
        )

    if set(["gal_lon", "gal_lat"]).issubset(table_read.columns):

        table_gal_to_loc = kc.transform_to_new_frame(
            table_read, "galactic", "ParticleFrame", detector_, detector_to_
        )
        table_gal_to_eq = kc.transform_to_new_frame(
            table_read, "galactic", "equatorial", detector_, detector_to_
        )
        table_gal_to_utm = kc.transform_to_new_frame(
            table_read, "galactic", "UTM", detector_, detector_to_
        )

    # testing angle separation
    if set(["phi", "theta"]).issubset(table_read.columns):

        if set(["azimuth", "zenith"]).issubset(table_read.columns):
            sep_utm_to_loc = test_benchmark_conversion(
                table_loc_to_utm, table_utm_to_loc
            )

            mean_ = sep_utm_to_loc.mean()
            min_ = sep_utm_to_loc.min()
            max_ = sep_utm_to_loc.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["RA-J2000", "DEC-J2000"]).issubset(table_read.columns):
            sep_eq_to_loc = test_benchmark_conversion(table_loc_to_eq, table_eq_to_loc)

            mean_ = sep_eq_to_loc.mean()
            min_ = sep_eq_to_loc.min()
            max_ = sep_eq_to_loc.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["gal_lon", "gal_lat"]).issubset(table_read.columns):

            sep_gal_to_loc = test_benchmark_conversion(
                table_loc_to_gal, table_gal_to_loc
            )

            mean_ = sep_gal_to_loc.mean()
            min_ = sep_gal_to_loc.min()
            max_ = sep_gal_to_loc.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

    if set(["azimuth", "zenith"]).issubset(table_read.columns):

        if set(["phi", "theta"]).issubset(table_read.columns):
            sep_loc_to_utm = test_benchmark_conversion(
                table_utm_to_loc, table_loc_to_utm
            )

            mean_ = sep_loc_to_utm.mean()
            min_ = sep_loc_to_utm.min()
            max_ = sep_loc_to_utm.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["RA-J2000", "DEC-J2000"]).issubset(table_read.columns):
            sep_eq_to_utm = test_benchmark_conversion(table_utm_to_eq, table_eq_to_utm)

            mean_ = sep_eq_to_utm.mean()
            min_ = sep_eq_to_utm.min()
            max_ = sep_eq_to_utm.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["gal_lon", "gal_lat"]).issubset(table_read.columns):
            sep_gal_to_utm = test_benchmark_conversion(
                table_utm_to_gal, table_gal_to_utm
            )

            mean_ = sep_gal_to_utm.mean()
            min_ = sep_gal_to_utm.min()
            max_ = sep_gal_to_utm.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

    if set(["RA-J2000", "DEC-J2000"]).issubset(table_read.columns):

        if set(["phi", "theta"]).issubset(table_read.columns):
            sep_loc_to_eq = test_benchmark_conversion(table_eq_to_loc, table_loc_to_eq)

            mean_ = sep_loc_to_eq.mean()
            min_ = sep_loc_to_eq.min()
            max_ = sep_loc_to_eq.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["azimuth", "zenith"]).issubset(table_read.columns):
            sep_utm_to_eq = test_benchmark_conversion(table_eq_to_utm, table_utm_to_eq)

            mean_ = sep_utm_to_eq.mean()
            min_ = sep_utm_to_eq.min()
            max_ = sep_utm_to_eq.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["gal_lon", "gal_lat"]).issubset(table_read.columns):
            sep_gal_to_eq = test_benchmark_conversion(table_eq_to_gal, table_gal_to_eq)

            mean_ = sep_gal_to_eq.mean()
            min_ = sep_gal_to_eq.min()
            max_ = sep_gal_to_eq.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

    if set(["gal_lon", "gal_lat"]).issubset(table_read.columns):

        if set(["phi", "theta"]).issubset(table_read.columns):
            sep_loc_to_gal = test_benchmark_conversion(
                table_gal_to_loc, table_loc_to_gal
            )

            mean_ = sep_loc_to_gal.mean()
            min_ = sep_loc_to_gal.min()
            max_ = sep_loc_to_gal.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["azimuth", "zenith"]).issubset(table_read.columns):
            sep_utm_to_gal = test_benchmark_conversion(
                table_gal_to_utm, table_utm_to_gal
            )

            mean_ = sep_utm_to_gal.mean()
            min_ = sep_utm_to_gal.min()
            max_ = sep_utm_to_gal.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )

        if set(["RA-J2000", "DEC-J2000"]).issubset(table_read.columns):
            sep_eq_to_gal = test_benchmark_conversion(table_gal_to_eq, table_eq_to_gal)

            mean_ = sep_eq_to_gal.mean()
            min_ = sep_eq_to_gal.min()
            max_ = sep_eq_to_gal.max()

            if max_ > angle_treshold:
                raise AssertionError(
                    "Error: Maximum angle separation = "
                    + str(max_)
                    + " > "
                    + str(angle_treshold)
                )
