"""Time conversion utilities.

For random time samples, goto `km3flux.random`
"""
from datetime import datetime

import numpy as np
from astropy.time import Time


def now():
    """Returns the time of now as astropy Time"""
    return Time(datetime.utcnow())


def np_to_datetime(intime):
    """Convert numpy/pandas datetime64 to list[datetime]."""
    nptime = np.atleast_1d(intime)
    np_corr = (nptime - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    return [datetime.utcfromtimestamp(t) for t in np_corr]


def np_to_astrotime(intime):
    return Time(np_to_datetime(intime))
