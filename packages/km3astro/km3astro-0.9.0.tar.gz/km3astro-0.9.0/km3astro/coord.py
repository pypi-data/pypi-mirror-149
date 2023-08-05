"""Coordinate transformations.

Galactic:
    GC at (0, 0),
    gal. longitude, latitude (l, b)

Horizontal / altaz (km3):
    centered at detector position
    altitude, azimuth (altitude = 90deg - zenith)

EquatorialJ200 / FK5 / ICRS / GCRS
    (right ascension, declination)

    Equatorial is the same as FK5. FK5 is superseded by the ICRS, so use
    this instead. Note that FK5/ICRS are _barycentric_ implementations,
    so if you are looking for *geocentric* equatorial (i.e.
    for solar system bodies), use GCRS.


A note on maing conventions:
``phi`` and ``theta`` refer to neutrino directions, ``azimuth`` and
``zenith`` to source directions (i.e. the inversed neutrino direction).
The former says where the neutrino points to, the latter says where it comes
from.

Also radian is the default. Degree can be used, but generally the default is
to assume radian.
"""
from astropy import units as u
from astropy.units import rad, deg, hourangle  # noqa
from astropy.coordinates import (
    EarthLocation,
    SkyCoord,
    AltAz,
    Longitude,
    Latitude,
    get_sun,
    get_moon,
)
import astropy.time
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.time import Time
from astropy.coordinates import Angle

import numpy as np
import pandas as pd
import numbers

# also import get_location and convergence_angle that has been shifted to km3frame
import km3astro.frame as kf

from km3astro.constants import (
    arca_longitude,
    arca_latitude,
    arca_height,
    orca_longitude,
    orca_latitude,
    orca_height,
    antares_longitude,
    antares_latitude,
    antares_height,
)
from km3astro.time import np_to_astrotime
from km3astro.random import random_date, random_azimuth
from km3astro.sources import GALACTIC_CENTER


def neutrino_to_source_direction(phi, theta, radian=True):
    """Flip the direction.

    Parameters
    ----------
    phi, theta: neutrino direction
    radian: bool [default=True]
        receive + return angles in radian? (if false, use degree)

    """
    phi = np.atleast_1d(phi).copy()
    theta = np.atleast_1d(theta).copy()
    if not radian:
        phi *= np.pi / 180
        theta *= np.pi / 180
    assert np.all(phi <= 2 * np.pi)
    assert np.all(theta <= np.pi)
    azimuth = (phi + np.pi) % (2 * np.pi)
    zenith = np.pi - theta
    if not radian:
        azimuth *= 180 / np.pi
        zenith *= 180 / np.pi
    return azimuth, zenith


def source_to_neutrino_direction(azimuth, zenith, radian=True):
    """Flip the direction.

    Parameters
    ----------
    zenith : float
        neutrino origin
    azimuth: float
        neutrino origin
    radian: bool [default=True]
        receive + return angles in radian? (if false, use degree)

    """
    azimuth = np.atleast_1d(azimuth).copy()
    zenith = np.atleast_1d(zenith).copy()
    if not radian:
        azimuth *= np.pi / 180
        zenith *= np.pi / 180
    phi = (azimuth - np.pi) % (2 * np.pi)
    theta = np.pi - zenith
    if not radian:
        phi *= 180 / np.pi
        theta *= 180 / np.pi
    return phi, theta


def Sun(time):
    """Wrapper around astropy's get_sun, accepting numpy/pandas time objects."""
    if not isinstance(time, astropy.time.Time):
        # if np.datetime64, convert to astro time
        time = np_to_astrotime(time)
    return get_sun(time)


def Moon(time):
    """Wrapper around astropy's get_moon, accepting numpy/pandas time objects."""
    if not isinstance(time, astropy.time.Time):
        # if np.datetime64, convert to astro time
        time = np_to_astrotime(time)
    return get_moon(time)


def local_frame(time, location):
    """Get the (horizontal) coordinate frame of your detector."""
    if not isinstance(time, astropy.time.Time):
        # if np.datetime64, convert to astro time
        time = np_to_astrotime(time)
    loc = kf.get_location(location)
    frame = AltAz(obstime=time, location=loc)
    return frame


def local_event(azimuth, time, zenith, location, radian=True, **kwargs):
    """Create astropy events from detector coordinates."""
    zenith = np.atleast_1d(zenith).copy()
    azimuth = np.atleast_1d(azimuth).copy()
    if not radian:
        azimuth *= np.pi / 180
        zenith *= np.pi / 180
    altitude = zenith - np.pi / 2

    loc = kf.get_location(location)
    # neutrino telescopes call the co-azimuth "azimuth"
    true_azimuth = (
        np.pi / 2 - azimuth + np.pi + kf.convergence_angle(loc.lat.rad, loc.lon.rad)
    ) % (2 * np.pi)
    frame = local_frame(time, location=location)
    event = SkyCoord(alt=altitude * rad, az=true_azimuth * rad, frame=frame, **kwargs)
    return event


def sun_local(time, loc):
    """Sun position in local coordinates."""
    frame = local_frame(time, location=loc)
    sun = Sun(time)
    sun_local = sun.transform_to(frame)
    return sun_local


def moon_local(time, loc):
    """Moon position in local coordinates."""
    frame = local_frame(time, location=loc)
    moon = Moon(time)
    moon_local = moon.transform_to(frame)
    return moon_local


def gc_in_local(time, loc):
    """Galactic center position in local coordinates."""
    frame = local_frame(time, location=loc)
    gc = GALACTIC_CENTER
    gc_local = gc.transform_to(frame)
    return gc_local


def orca_gc_dist(azimuth, time, zenith, frame="detector"):
    """Return angular distance of event to GC.

    Parameters
    ==========
    frame: str, [default: 'detector']
        valid are 'detector', 'galactic', 'icrs', 'gcrs'
    """
    evt = local_event(azimuth, time, zenith)
    galcen = gc_in_local(time, loc)
    if frame == "detector":
        pass
    elif frame in ("galactic", "icrs", "gcrs"):
        evt = evt.transform_to(frame)
        galcen = galcen.transform_to(frame)
    return evt.separation(galcen).radian


def orca_sun_dist(azimuth, time, zenith):
    """Return distance of event to sun, in detector coordinates."""
    evt = local_event(azimuth, time, zenith)
    sun = sun_local(time, loc)
    dist = evt.separation(sun).radian
    return dist


def gc_dist_random(zenith, frame="detector"):
    """Generate random (time, azimuth) events and get distance to GC."""
    n_evts = len(zenith)
    time = random_date(n=n_evts)
    azimuth = random_azimuth(n=n_evts)
    dist = orca_gc_dist(azimuth, time, zenith, frame=frame)
    return dist


def sun_dist_random(zenith):
    """Generate random (time, azimuth) events and get distance to GC."""
    n_evts = len(zenith)
    time = random_date(n=n_evts)
    azimuth = random_azimuth(n=n_evts)
    dist = orca_sun_dist(azimuth, time, zenith)
    return dist


class Event(object):
    def __init__(self, zenith, azimuth, time, location):
        self.zenith = zenith
        self.azimuth = azimuth
        self.time = time

    @classmethod
    def from_zenith(cls, zenith, **initargs):
        zenith = np.atleast_1d(zenith)
        n_evts = zenith.shape[0]
        azimuth = random_azimuth(n_evts)
        time = random_date(n_evts)
        return cls(zenith, azimuth, time, **initargs)


def is_args_fine_for_frame(frame, *args):

    if frame == "ParticleFrame" and len(args) != 6:
        raise TypeError(
            "Only "
            + str(len(args))
            + " given when 6 are needed: date, time, theta, phi, unit, particleframe ! for ParticleFrame"
        )

    if frame == "UTM" and len(args) != 6:
        raise TypeError(
            "Only "
            + str(len(args))
            + " given when 6 are needed: date, time, azimuth, zenith, unit, particleframe ! for UTM"
        )

    if frame == "equatorial" and len(args) != 4:
        raise TypeError(
            "Only "
            + str(len(args))
            + " given when 4 are needed: date, time, ra, dec ! for Equatorial"
        )

    if frame == "galactic" and len(args) != 4:
        raise TypeError(
            "Only "
            + str(len(args))
            + " given when 4 are needed: date, time, l, b ! for Galactic"
        )

    return 0


def build_event(Cframe, *args):

    is_args_fine_for_frame(Cframe, *args)

    # Defining time of observation
    # using astropy.time Time because pandas.to_datetime raise an error for convertion in np_to_astrotime
    time = args[0] + "T" + args[1]
    time = Time(time)

    # ParticleFrame : date, time , theta, phi, unit, detector_name
    if Cframe == "ParticleFrame":

        theta = args[2]
        phi = args[3]
        unit = args[4]
        if unit == "deg":
            phi = phi * u.deg
            theta = theta * u.deg

        else:
            phi = phi * u.rad
            theta = theta * u.rad

        loc = kf.get_location(args[5])
        r = u.Quantity(100, u.m)  # dummy r value ! Warning !
        return SkyCoord(
            frame=kf.ParticleFrame,
            phi=phi,
            theta=theta,
            location=loc,
            obstime=time,
            r=r,
        )

    # UTM : date, time, azimuth, zenith, unit, detector
    elif Cframe == "UTM":

        az = args[2]
        zenith = args[3]
        unit = args[4]
        if unit == "deg":
            az = az * u.deg
            zenith = zenith * u.deg

        else:
            az = az * u.rad
            zenith = zenith * u.rad

        loc = kf.get_location(args[5])
        r = u.Quantity(100, u.m)  # dummy r value ! Warning !

        return SkyCoord(
            frame=kf.UTM, azimuth=az, zenith=zenith, location=loc, obstime=time, r=r
        )

    elif Cframe == "galactic":
        l = args[2]
        b = args[3]

        if isinstance(l, str):
            l = Angle(l, unit="hourangle")
        elif isinstance(l, numbers.Number):
            l = Angle(l, unit=u.deg)

        if isinstance(b, str):
            b = Angle(b, unit="hourangle")
        elif isinstance(b, numbers.Number):
            b = Angle(b, unit=u.deg)

        return SkyCoord(frame=Cframe, l=l, b=b, unit="deg", obstime=time)

    elif Cframe == "equatorial":
        ra = args[2]
        dec = args[3]

        if isinstance(ra, str):
            ra = Angle(ra, unit="hourangle")
        elif isinstance(ra, numbers.Number):
            ra = Angle(ra, unit=u.deg)

        if isinstance(dec, str):
            dec = Angle(dec, unit=u.deg)
        elif isinstance(dec, numbers.Number):
            dec = Angle(dec, unit=u.deg)

        return SkyCoord(frame=ICRS, ra=ra, dec=dec, obstime=time)

    else:
        raise ValueError("Error: Wrong Frame input:" + Cframe)
        return None


def transform_to(Skycoord, frame_to, detector_to="antares"):

    time = Skycoord.obstime
    loc = kf.get_location(detector_to)

    if frame_to == "ParticleFrame":

        frame = kf.ParticleFrame(obstime=time, location=loc)
        return Skycoord.transform_to(frame)

    elif frame_to == "UTM":
        frame = kf.UTM(obstime=time, location=loc)
        return Skycoord.transform_to(frame)

    elif frame_to == "altaz":
        frame = AltAz(obstime=time, location=loc)
        return Skycoord.transform_to(frame)

    elif frame_to == "equatorial":
        return Skycoord.transform_to(ICRS)

    elif frame_to == "galactic":
        return Skycoord.transform_to("galactic")

    else:
        raise ValueError("Wrong Frame to transform: " + frame_to + " is not valid")
        return -1


def transform_to_new_frame(
    table, frame_, frame_to, detector="antares", detector_to="antares"
):

    if frame_ == "ParticleFrame":
        list_evt = table.apply(
            lambda x: build_event(
                frame_, x.date, x.time, x.theta, x.phi, "deg", detector
            ),
            axis=1,
            result_type="expand",
        )

    if frame_ == "UTM":
        list_evt = table.apply(
            lambda x: build_event(
                frame_, x.date, x.time, x.azimuth, x.zenith, "deg", detector
            ),
            axis=1,
            result_type="expand",
        )

    if frame_ == "equatorial":
        list_evt = table.apply(
            lambda x: build_event(
                frame_, x.date, x.time, x["RA-J2000"], x["DEC-J2000"]
            ),
            axis=1,
            result_type="expand",
        )

    if frame_ == "galactic":
        list_evt = table.apply(
            lambda x: build_event(frame_, x.date, x.time, x.gal_lon, x.gal_lat),
            axis=1,
            result_type="expand",
        )

    if isinstance(list_evt, pd.Series):
        series_ = {"SkyCoord_base": list_evt}
        list_evt = pd.DataFrame(series_)

    list_evt.set_axis(["SkyCoord_base"], axis="columns", inplace=True)

    list_evt["SkyCoord_new"] = list_evt.apply(
        lambda x: transform_to(x.SkyCoord_base, frame_to, detector_to),
        axis=1,
        result_type="expand",
    )

    return list_evt


def print_Skycoord(SkyCoord):
    print(SkyCoord)


def reader_from_file(file):

    table = pd.read_csv(file, comment="#")

    return table


def get_az_zenith(SC, detector_="antares", unit="deg"):

    SC_copy = SC.copy()
    loc = kf.get_location(detector_)

    if SC.frame.name != "utm":
        raise ValueError("Wrong Frame: Expected 'utm' but got " + SC.frame.name)

    # if SC.frame.name != "utm":
    # SC_copy = transform_to(SC, "UTM", detector_)

    zenith = SC_copy.zenith.rad
    az = SC_copy.azimuth.rad

    if unit == "deg":
        zenith = SC_copy.zenith.deg
        az = SC_copy.azimuth.deg

    return az, zenith


def get_phi_theta(SC, detector_="antares", unit="deg"):

    SC_copy = SC.copy()
    loc = kf.get_location(detector_)

    if SC.frame.name != "particleframe":
        raise ValueError(
            "Wrong Frame: Expected 'particleframe' but got " + SC.frame.name
        )

    # if SC.frame.name != "particleframe":
    # SC_copy = transform_to(SC, "ParticleFrame", detector_)

    phi = SC_copy.phi.rad
    theta = SC_copy.theta.rad

    if unit == "deg":
        phi = SC_copy.phi.deg
        theta = SC_copy.theta.deg

    return phi, theta


def get_alt_az(SC, unit="deg"):

    if SC.frame.name != "altaz":
        raise Exception("Wrong Frame: Expected altAz but got " + SC.frame.name)

    alt = SC.alt
    az = SC.az

    if unit == "deg":
        alt = SC.alt.deg
        az = SC.az.deg

    return alt, az


def get_ra_dec(SC, unit="deg"):

    if SC.frame.name != "icrs" and SC.frame.name != "fk5":
        raise Exception("Wrong Frame: Expected icrs or fk5 but got " + SC.frame.name)

    ra = SC.ra
    dec = SC.dec

    if unit == "deg":
        ra = SC.ra.deg
        dec = SC.dec.deg

    if unit == "hourangle":
        ra = Angle(ra, unit="hourangle")
        ra = ra.to_string()
        dec = dec

    return ra, dec


def get_l_b(SC, unit="deg"):

    if SC.frame.name != "galactic":
        raise ValueError("Wrong Frame: Expected galactic but got " + SC.frame.name)

    l = SC.l
    b = SC.b

    if unit == "deg":
        l = SC.l.deg
        b = SC.b.deg

    return l, b
