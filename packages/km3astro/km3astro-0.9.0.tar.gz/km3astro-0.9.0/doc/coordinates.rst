Coordinates
===========

Antares
-------

see
http://antares.in2p3.fr/internal/dokuwiki/doku.php?id=astro_coordinatetransformation_howto

Conventions + Definitions
-------------------------

Neutrino direction vs Source Direction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We usually talk about the direction a neutrino is *going to*. When
determining which source it came from, we obviously need to invert the
direction.

Neutrino direction, polar coordinates: \*theta\* and \*phi\*

Neutrino source: \*zenith\* and \*azimuth\*

Azimuth Definition
~~~~~~~~~~~~~~~~~~

Our definition of the azimuth angle differs from the more common
definition that is used in SLALIB, SeaTray's astro package, and astropy
(used in km3astro).

::

    true_azimuth = (90deg - azimuth) mod 360deg

Equatorial Coordinates
~~~~~~~~~~~~~~~~~~~~~~

Equatorial coordinates are ICRS, i.e. J2000 Epoch, J2000 Equinox,
Barycentric (barycenter of Solar system as coordinate origin).

If you'd rather have geocentric equatorial coordinates, use GCRS.

If you are looking for “J2000 Equatorial coordinates” you probably want
ICRS and not FK5.

For more details on ICRS, see
https://en.wikipedia.org/wiki/International_Celestial_Reference_System
and maybe
http://docs.astropy.org/en/stable/api/astropy.coordinates.ICRS.html#astropy.coordinates.ICRS
.

UTM Grid
~~~~~~~~

The UTM origin is noted at the head of the .detx v2 files:
`Dataformats#Detector\_Description\_.28.detx.29 <Dataformats#Detector_Description_.28.detx.29>`__

A snapshot of these (July 2017) can be found at ``km3astro.constants``.

Benchmarks
----------

Antares ``astro`` benchmarks:
http://antares.in2p3.fr/internal/dokuwiki/doku.php?id=benchmarks_astro

(Partial) replication with ``km3astro``: :ref:`sphx_glr_auto_examples_plot_benchmarks.py`
