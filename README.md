[![Coverage
Status](https://coveralls.io/repos/github/drvinceknight/Nashpy/badge.svg?branch=master)](https://coveralls.io/github/drvinceknight/Nashpy?branch=master)
[![Build
Status](https://travis-ci.org/drvinceknight/Nashpy.svg?branch=master)](https://travis-ci.org/drvinceknight/Nashpy)
[![Build
status](https://ci.appveyor.com/api/projects/status/fj864wcbfpqfy6po?svg=true)](https://ci.appveyor.com/project/drvinceknight/nashpy)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.164954.svg)](https://doi.org/10.5281/zenodo.164954)
[![Join the chat at
https://gitter.im/Nashpy/Lobby](https://badges.gitter.im/Nashpy/Lobby.svg)](https://gitter.im/Nashpy/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# Nash: a python library for the computation of equilibria of 2 player strategic games.

**This is a library with simple dependencies (it only requires numpy and scipy)
so that it is pip installable: if you want to do sophisticated equilibria
computation YOU SHOULD use [gambit](https://github.com/gambitproject/gambit).**

This is an implementation of the following algorithms for equilibria of 2 player
games:

- Support enumeration
- Best response polytope vertex enumeration
- Lemke Howson algorithm

## Installation

The easiest way to install is from pypi:

```bash
$ pip install nashpy
```

## Usage

Create bi matrix games by passing two 2 dimensional arrays/lists:

```python
>>> import nash
>>> A = [[1, 2], [3, 0]]
>>> B = [[0, 2], [3, 1]]
>>> battle_of_the_sexes = nash.Game(A, B)
>>> for eq in battle_of_the_sexes.support_enumeration():
...     print(eq)
(array([ 1.,  0.]), array([ 0.,  1.]))
(array([ 0.,  1.]), array([ 1.,  0.]))
(array([ 0.5,  0.5]), array([ 0.5,  0.5]))
>>> battle_of_the_sexes[[0, 1], [1, 0]]
array([3, 3])

```

## Documentation

Full documentation is available here: http://nashpy.readthedocs.io/

## Development

To install a development version of this library:

```
$ python setup.py develop
```

To run the full test suite:

```
$ python setup.py test
```

All contributions are welcome, although this is meant to be a simple library,
for more detailed game theoretic contribution please see
[gambit](https://github.com/gambitproject/gambit).

## Code of conduct

In the interest of fostering an open and welcoming environment, all
contributors, maintainers and users are expected to abide by the Python code of
conduct: https://www.python.org/psf/codeofconduct/
