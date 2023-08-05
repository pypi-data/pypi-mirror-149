#!/usr/bin/env python
# Filename: setup.py
"""
km3astro setup script.

"""
import os
from setuptools import setup
import sys


def read_requirements(kind):
    """Return a list of stripped lines from a file"""
    with open(os.path.join("requirements", kind + ".txt")) as fobj:
        requirements = [l.strip() for l in fobj.readlines()]
    v = sys.version_info
    if (v.major, v.minor) < (3, 6):
        try:
            requirements.pop(requirements.index("black"))
        except ValueError:
            pass
    return requirements


try:
    with open("README.rst") as fh:
        long_description = fh.read()
except UnicodeDecodeError:
    long_description = "km3astro - astronomical utilities for KM3NeT"

setup(
    name="km3astro",
    url="http://git.km3net.de/km3py/km3astro",
    description="Astronomical utilities for KM3NeT",
    long_description=long_description,
    author="Tamas Gal and Moritz Lotze",
    author_email="tgal@km3net.de",
    packages=["km3astro"],
    include_package_data=True,
    platforms="any",
    setup_requires=["numpy>=1.12", "setuptools_scm"],
    install_requires=read_requirements("install"),
    extras_require={kind: read_requirements(kind) for kind in ["dev", "extras"]},
    use_scm_version=True,
    python_requires=">=3.5",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
    ],
)

__author__ = "Tamas Gal and Moritz Lotze"
