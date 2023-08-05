"""
===============================
Local to Equatorial Coordinates
===============================

Where do my neutrinos come from?
"""

# sphinx_gallery_thumbnail_number = 3

__author__ = "moritz"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from km3astro.coord import local_event, neutrino_to_source_direction
from km3astro.frame import get_location
from km3astro.plot import plot_equatorial
from km3astro.sources import VELA_X


##########################################################
# Detector Coordinates
# --------------------
# Let's define some random events.

theta = 10 * np.pi / 180
phi = 8 * np.pi / 180
time = pd.to_datetime(
    [
        "2015-01-12T15:10:12",
        "2015-03-15T14:24:01",
    ]
).values[0]

##########################################################
# Phi, theta: Where the neutrino is pointing to
#
# Zenith, azimuth: where the neutrino is coming from

azimuth, zenith = neutrino_to_source_direction(phi, theta, radian=True)

#########################################################################
# We want to observe them from the Orca location. Let's look at our
# geographical coordinates.
#
# In km3astro, there are the predefined locations "orca", "arca" and "antares".
orca_loc = get_location("orca")

#########################################################################
# Create event in local coordinates (aka AltAz or Horizontal Coordinates)
#
# This returns an ``astropy.SkyCoord`` instance.

evt_local = local_event(azimuth=azimuth, zenith=zenith, time=time, location="orca")

print(evt_local)

##############################################################
# Transform to equatorial -- ICRS
# -------------------------------
#
# "If you’re looking for “J2000” coordinates, and aren’t sure if
# you want to use this or FK5, you probably want to use ICRS. It’s more
# well-defined as a catalog coordinate and is an inertial system, and is
# very close (within tens of milliarcseconds) to J2000 equatorial."

evt_equat = evt_local.transform_to("icrs")
print(evt_equat)

##############################################################
# How far removed are these events from a certain source?

source_dist = evt_equat.separation(VELA_X)

plt.hist(source_dist.degree, bins="auto")

##############################################################
# Plot them in a square

right_ascension_radian = evt_equat.ra.rad
declination_radian = evt_equat.dec.rad

plt.scatter(right_ascension_radian, declination_radian)
plt.scatter(VELA_X.ra.rad, VELA_X.dec.rad)
plt.xlabel("Right Ascension / rad")
plt.ylabel("Declination / rad")

##############################################################
# Plot them in a skymap.
#
# We need this little wrap because astropy's
# convention for ra, dec differs from matplotlib.

ax = plot_equatorial(evt_equat, markersize=12, label="Event")
plot_equatorial(VELA_X, markersize=12, ax=ax, label="Vela X")
plt.legend(loc="best")
