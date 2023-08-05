#!/usr/bin/env python
"""Test whether at some time the sun is below the horizon in ORCA."""

import os.path

import numpy as np
import km3astro
import km3astro.extras

from ..random import random_date


DATADIR = os.path.join(os.path.dirname(km3astro.__file__), "data")


def above_horiz(times):
    pd = km3astro.extras.pandas()

    fname = os.path.join(DATADIR, "orca_sun_isup.h5")
    with pd.HDFStore(fname) as h5:
        o_rise = h5["o_rise"].values
        o_set = h5["o_set"].values
    return [(t >= o_rise) & (t <= o_set) for t in times]


def is_below(times):
    ab = np.array(above_horiz(times))
    risen = np.logical_not(np.sum(ab, axis=1))
    return risen


def random_time_sun_vis(n=1, keep_above=False, **kwargs):
    ngen = n * 3
    dates = random_date(n=ngen, **kwargs)
    mask = is_below(dates)
    if keep_above:
        mask = np.logical_not(mask)
    dates = dates[mask]
    if len(dates) < n:
        dates = random_time_sun_vis(n * 2, keep_above=keep_above, **kwargs)
    return dates[:n]
