import doctest
import os
import unittest

from setuptools import find_packages, setup

# Read in the version number
exec(open("src/nashpy/version.py", "r").read())

requirements = ["numpy>=1.12.1", "scipy>=0.19.0"]


setup(
    name="nashpy",
    version=__version__,
    install_requires=requirements,
    author="Vince Knight, James Campbell",
    author_email=("knightva@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
    description="A library to compute equilibria of 2 player normal form games",
)
