import numpy as np

from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
import astropy.units as u
from astropy.units import rad, deg, hourangle  # noqa

from astropy.coordinates import Angle

from astropy.coordinates import (
    EarthLocation,
    SkyCoord,
    AltAz,
    Longitude,
    Latitude,
)

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


from astropy.coordinates import BaseCoordinateFrame
import astropy.coordinates.representation as rep
from astropy.coordinates import RepresentationMapping
from astropy.coordinates.attributes import (
    TimeAttribute,
    EarthLocationAttribute,
    QuantityAttribute,
)
from astropy.coordinates import TransformGraph, frame_transform_graph, FunctionTransform


LOCATIONS = {
    "arca": EarthLocation.from_geodetic(
        lon=Longitude(arca_longitude * deg),
        lat=Latitude(arca_latitude * deg),
        height=arca_height,
    ),
    "orca": EarthLocation.from_geodetic(
        lon=Longitude(orca_longitude * deg),
        lat=Latitude(orca_latitude * deg),
        height=orca_height,
    ),
    "antares": EarthLocation.from_geodetic(
        lon=Longitude(antares_longitude * deg),
        lat=Latitude(antares_latitude * deg),
        height=antares_height,
    ),
}


def get_location(location):
    try:
        loc = LOCATIONS[location]
    except KeyError:
        raise KeyError("Invalid location, valid are 'orca', 'arca', 'antares'")
    return loc


def convergence_angle(lat, lon):
    """Calculate the converge angle on the UTM grid.

    Parameters
    ----------
    lon : number
        Longitude in rad
    lat : number
        Latitude in rad

    """
    latitude_deg = lat * u.deg

    if latitude_deg > 84 * u.deg or latitude_deg < -80 * u.deg:
        raise ValueError(
            "UTM coordinate system is only defined between -80deg S and 84deg N."
        )

    # detector position, longitude and latitude in rad
    # lambda  = longitude
    phi = lat

    # find UTM zone and central meridian

    # longitude of the central meridian of UTM zone in rad
    lambda0 = longitude_of_central_meridian(utm_zone(lon))
    omega = lon - lambda0

    # parameters of the Earth ellipsoid
    sma = 6378137  # semi-major axis in meters (WGS84)
    ecc = 0.0066943800  # eccentricity (WGS84)

    rho = sma * (1 - ecc) / pow(1 - ecc * np.sin(phi) ** 2, 3 / 2)
    nu = sma / np.sqrt(1 - ecc * np.sin(phi) ** 2)
    psi = nu / rho
    t = np.tan(phi)

    angle = (
        np.sin(phi) * omega
        - np.sin(phi) * omega ** 3 / 3 * pow(np.cos(phi), 2) * (2 * psi ** 2 - psi)
        - np.sin(phi)
        * omega ** 5
        / 15
        * pow(np.cos(phi), 4)
        * (
            psi ** 4 * (11 - 24 * t ** 2)
            - psi ** 3 * (11 - 36 * t ** 2)
            + 2 * psi ** 2 * (1 - 7 * t ** 2)
            + psi * t ** 2
        )
        - np.sin(phi)
        * omega ** 7
        / 315
        * pow(np.cos(phi), 6)
        * (17 - 26 * t ** 2 + 2 * t ** 4)
    )

    return angle


def utm_zone(lat):
    """The UTM zone for a given latitude

    Parameters
    ----------
    lat : number
        Latitude in rad

    """
    return 1 + int((np.pi + lat) / (6 * np.pi / 180))


def longitude_of_central_meridian(utmzone):
    """The longitude of the central meridian for a given UTM zone.

    Parameters
    ----------
    utmzone : number
        The UTM zone.

    """
    zone_width = 6 * np.pi / 180
    return -np.pi + (utmzone - 1) * zone_width + zone_width / 2


class ParticleFrame(BaseCoordinateFrame):
    default_representation = rep.PhysicsSphericalRepresentation

    # Specify frame attributes required to fully specify the frame
    obstime = TimeAttribute(default=None)
    location = EarthLocationAttribute(default=get_location("arca"))


class UTM(BaseCoordinateFrame):

    default_representation = rep.PhysicsSphericalRepresentation

    frame_specific_representation_info = {
        rep.PhysicsSphericalRepresentation: [
            RepresentationMapping("phi", "azimuth"),
            RepresentationMapping("theta", "zenith"),
        ]
    }

    obstime = TimeAttribute(default=None)
    location = EarthLocationAttribute(default=get_location("arca"))

    @property
    def alt_utm(self):
        """Altitude in UTM"""
        return Angle(np.pi / 2 - self.zenith.rad, u.rad)


@frame_transform_graph.transform(FunctionTransform, ParticleFrame, AltAz)
def ParticleFrame_to_AltAz(ParticleFrame_, altaz):

    phi = ParticleFrame_.phi.rad
    theta = ParticleFrame_.theta.rad
    loc = ParticleFrame_.location
    time = ParticleFrame_.obstime

    conv_angle = Angle(convergence_angle(loc.lat.rad, loc.lon.rad), unit=u.radian)

    altitude = theta - np.pi / 2
    Corrected_azimuth = (np.pi / 2 - phi + np.pi + conv_angle.rad) % (2 * np.pi)

    altaz = AltAz(
        alt=altitude * rad, az=Corrected_azimuth * rad, obstime=time, location=loc
    )

    return altaz


@frame_transform_graph.transform(FunctionTransform, AltAz, ParticleFrame)
def AltAz_to_ParticleFrame(altaz_, particleframe_):

    alt = altaz_.alt.rad
    az = altaz_.az.rad
    loc = altaz_.location
    time = altaz_.obstime
    r = u.Quantity(
        100, u.m
    )  # Warning dummy r value! For SphericalRepresentation to PhysicsSphericalRepresentation conversion

    conv_angle = Angle(convergence_angle(loc.lat.rad, loc.lon.rad), unit=u.radian)

    phi = np.pi / 2 + np.pi + conv_angle.rad - az

    theta = alt + np.pi / 2

    particleframe_ = ParticleFrame(
        phi=phi * rad, theta=theta * rad, obstime=time, location=loc, r=r
    )

    return particleframe_


# UTM: X = Easting, Y = Northing with  Northing = North + conv_angle
# Altaz: X = North Y = East


@frame_transform_graph.transform(FunctionTransform, UTM, AltAz)
def UTM_to_AltAz(UTM_, altaz):

    az = UTM_.azimuth.rad
    ze = UTM_.zenith.rad

    loc = UTM_.location
    time = UTM_.obstime

    conv_angle = Angle(convergence_angle(loc.lat.rad, loc.lon.rad), unit=u.radian)

    altitude = np.pi / 2 - ze
    Corrected_azimuth = (np.pi / 2 - az + conv_angle.rad) % (2 * np.pi)

    altaz = AltAz(
        alt=altitude * rad, az=Corrected_azimuth * rad, obstime=time, location=loc
    )

    return altaz


@frame_transform_graph.transform(FunctionTransform, AltAz, UTM)
def AltAz_to_UTM(altaz_, UTM_):

    alt = altaz_.alt.rad
    caz = altaz_.az.rad

    loc = altaz_.location
    time = altaz_.obstime
    r = u.Quantity(
        100, u.m
    )  # Warning dummy r value! For SphericalRepresentation to PhysicsSphericalRepresentation.

    conv_angle = Angle(convergence_angle(loc.lat.rad, loc.lon.rad), unit=u.radian)

    az = 5 * np.pi / 2 + conv_angle.rad - caz
    az = az % (2 * np.pi)
    ze = np.pi / 2 - alt

    UTM_ = UTM(azimuth=az * rad, zenith=ze * rad, obstime=time, location=loc, r=r)
    return UTM_


@frame_transform_graph.transform(FunctionTransform, UTM, ParticleFrame)
def UTM_to_ParticleFrame(UTM_, particleframe):

    phi = UTM_.azimuth.rad - np.pi
    theta = np.pi - UTM_.zenith.rad
    loc = UTM_.location
    time = UTM_.obstime
    r = UTM_.r

    particleframe = ParticleFrame(
        phi=phi * rad, theta=theta * rad, obstime=time, location=loc, r=r
    )

    return particleframe


@frame_transform_graph.transform(FunctionTransform, ParticleFrame, UTM)
def ParticleFrame_to_UTM(particleframe, UTM_):

    az = particleframe.phi.rad + np.pi
    ze = np.pi - particleframe.theta.rad

    loc = particleframe.location
    time = particleframe.obstime
    r = particleframe.r

    UTM_ = UTM(azimuth=az * rad, zenith=ze * rad, obstime=time, location=loc, r=r)

    return UTM_
