from setuptools import setup, find_packages
import unittest
import doctest

# Read in the version number
exec(open('src/nash/version.py', 'r').read())

requirements = ["numpy"]

def test_suite():
    """Discover all tests in the tests dir"""
    test_loader = unittest.TestLoader()
    # Read in unit tests
    test_suite = test_loader.discover('tests')

    # Read in doctests from README
    test_suite.addTests(doctest.DocFileSuite('README.md',
                                             optionflags=doctest.ELLIPSIS))
    return test_suite

setup(
    name='nashpy',
    version=__version__,
    install_requires=requirements,
    author='Vince Knight, James Campbell',
    author_email=('knightva@cardiff.ac.uk'),
    packages=find_packages('src'),
    package_dir={"": "src"},
    test_suite='setup.test_suite',
    url='',
    license='The MIT License (MIT)',
    description='A library to compute equilibria of 2 player normal form games',
)
