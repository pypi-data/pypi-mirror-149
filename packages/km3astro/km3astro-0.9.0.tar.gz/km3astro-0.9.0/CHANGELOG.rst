Unreleased Changes
------------------

Version 0
---------

0.9.0 / 2022-05-02
~~~~~~~~~~~~~~~~~~
* Refactoring
* Coordinate transformation is now fully based on astropy.SkyCoord with
  a new frame designed for KM3NeT
* Bugfixes

0.8.4 / 2020-01-23
~~~~~~~~~~~~~~~~~~
* Cleanup and remove unnecessary requirements (scipy, km3pipe, ...)
* Bug fixes
* Preparation for API clean-up

0.8.3
~~~~~
* improve local -> equatorial example

0.8.2
~~~~~
* add fast sampling of times where sun is above/below horizon
* add new jenkins build
* more example
* bump all dependencies

0.8
~~~
* move a log of methods to km3pipe
* add a makefile

0.7.5
~~~~~
* add equat plotter

0.7.4
~~~~~
* bump km3pipe due to dataclass update
* polish examples a bit

0.7.3
~~~~~
* move minor stuff to km3pipe

0.7.1
~~~~~
* update examples
* fix builds
* streamline time handling

0.7
~~~
* COORDINATE FIX: what we call azimuth is actually co-azimuth
* add common sources

0.6
~~~
* add UTM coordinates
* derive arca coordinates from UTM grid

0.5
~~~
* fix lat-lon mixup bug
* add convenience methods for coord trafo

0.4.0
~~~~~
* move random sampling methods to `km3astro.random`

0.3.2
~~~~~
* add example gallery

0.3.0 / 2017-03-18
~~~~~~~~~~~~~~~~~~
* initial versioned release
* add package goodies
