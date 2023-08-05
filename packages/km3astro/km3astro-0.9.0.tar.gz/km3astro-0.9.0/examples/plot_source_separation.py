"""
===============================
Local to Equatorial Coordinates
===============================

Where do my neutrinos come from?
"""

__author__ = "moritz"

import numpy as np
import pandas as pd

from km3astro.coord import local_event, Sun, neutrino_to_source_direction


##########################################################
# Detector Coordinates
# --------------------
# Let's define some random events.

theta = np.array([10, 45, 70, 23, 20, 11, 24, 54]) * np.pi / 180
phi = np.array([4, 23, 200, 320, 10, 45, 29, 140]) * np.pi / 180
time = pd.to_datetime(
    [
        "2015-01-12T15:10:12",
        "2015-06-12T13:48:56",
        "2015-03-09T21:57:52",
        "2015-03-15T14:24:01",
        "2015-01-12T15:10:12",
        "2015-06-12T13:48:56",
        "2015-03-09T21:57:52",
        "2015-03-15T14:24:01",
    ]
).values


##########################################################
# Phi, theta: Where the neutrino is pointing to
#
# Zenith, azimuth: where the neutrino is coming from

azimuth, zenith = neutrino_to_source_direction(phi, theta, radian=True)

#########################################################################
# Create event in local coordinates (aka AltAz or Horizontal Coordinates)
#
# This returns an ``astropy.SkyCoord`` instance.

evt_local = local_event(azimuth=azimuth, zenith=zenith, time=time, location="orca")

sun = Sun(time)

sep = evt_local.separation(sun)

print(sep)
