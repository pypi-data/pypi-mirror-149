"""
========================
Sun in local coordinates
========================

Show off some coordinate transformations.
"""

# Author: Moritz Lotze <mlotze@km3net.de>
# License: BSD-3

from astropy.units import deg
import numpy as np
import pandas as pd

from km3astro.random import random_date, random_azimuth, random_zenith
from km3astro.coord import local_frame, Sun, source_to_neutrino_direction


##########################################################
# generate some random events

n_evts = 1e4
zen = random_zenith(n=n_evts)
time = random_date(n=n_evts)
azi = random_azimuth(n=n_evts)

##########################################################
# transform to horizontal coordinates

orca_frame = local_frame(time=time, location="orca")
sun = Sun(time)

sun_orca = sun.transform_to(orca_frame)

sun_azi = sun_orca.az.rad
sun_zen = (90 * deg - sun_orca.alt).rad

sun_phi, sun_theta = source_to_neutrino_direction(sun_azi, sun_zen)

sun_df = pd.DataFrame(
    {
        "Sun Azimuth": sun_azi,
        "Sun Zenith": sun_zen,
        "Sun Cos Zenith": np.cos(sun_zen),
        "Sun Phi": sun_phi,
        "Sun Theta": sun_theta,
        "Sun Cos Theta": np.cos(sun_theta),
    }
)

#########################################################

sun_df.plot.hexbin("Sun Zenith", "Sun Azimuth", cmap="viridis")


#########################################################

sun_df.plot.hexbin("Sun Cos Zenith", "Sun Azimuth", cmap="magma")

#########################################################

sun_df.plot.hexbin("Sun Theta", "Sun Phi", cmap="inferno")

#########################################################

sun_df.plot.hexbin("Sun Cos Theta", "Sun Phi", cmap="plasma")
