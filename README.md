[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.596758.svg)](https://doi.org/10.5281/zenodo.596758)
![](https://github.com/drvinceknight/Nashpy/workflows/CI/badge.svg)
[![Discord](https://img.shields.io/discord/753185848337367060?label=Discord)](https://discord.gg/wZsv6s8TTB)
[![Gitter](https://badges.gitter.im/drvinceknight/Nashpy.svg)](https://gitter.im/drvinceknight/Nashpy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![DOI](http://joss.theoj.org/papers/10.21105/joss.00904/status.svg)](https://doi.org/10.21105/joss.00904)

# Nashpy: a python library for the computation of equilibria of 2 player strategic games.

This library implements the following algorithms for Nash equilibria on 2 player
games:

- Support enumeration
- Best response polytope vertex enumeration
- Lemke Howson algorithm

**Nashpy** has a small set of Python dependencies: it only requires `numpy`
and `scipy` so is straightforward to install on all operating systems.

## Installation

```bash
$ python -m pip install nashpy
```

To install Nashpy on Fedora, use:

```sh
$ dnf install python3-nashpy
```

## Usage

<!--alex ignore bi-->

Create bi matrix games by passing two 2 dimensional arrays/lists:

```python
>>> import nashpy as nash
>>> A = [[1, 2], [3, 0]]
>>> B = [[0, 2], [3, 1]]
>>> game = nash.Game(A, B)
>>> for eq in game.support_enumeration():
...     print(eq)
(array([1., 0.]), array([0., 1.]))
(array([0., 1.]), array([1., 0.]))
(array([0.5, 0.5]), array([0.5, 0.5]))
>>> game[[0, 1], [1, 0]]
array([3, 3])

```
## Documentation

Full documentation is available here: http://nashpy.readthedocs.io/

## Other game theoretic software

- [Gambit](http://www.gambit-project.org/) is a library with a python api and
  support for more algorithms and more than 2 player games.
- [Game theory explorer](http://gte.csc.liv.ac.uk/index/) a web interface to
  gambit useful for teaching.
- [Axelrod](http://axelrod.readthedocs.io/en/stable/) a research library aimed
  at the study of the Iterated Prisoners dilemma


## Development

Clone the repository and create a virtual environment:

```bash
$ git clone https://github.com/drvinceknight/nashpy.git
$ cd nashpy
$ python -m venv env

```

Activate the virtual environment and install [`tox`](https://tox.readthedocs.io/en/latest/):

```bash
$ source env/bin/activate
$ python -m pip install tox

```

Make modifications.

To run the tests:

```bash
$ python -m tox

```

To build the documentation. First install the software which also installs the
documentation build requirements.

```bash
$ python -m pip install flit
$ python -m flit install --symlink
```

Then:

```bash
$ cd docs
$ make html
```

Full contribution documentation is available at
https://nashpy.readthedocs.io/en/latest/contributing/index.html 

Pull requests are welcome.

## Code of conduct

In the interest of fostering an open and welcoming environment, all
contributors, maintainers and users are expected to abide by the Python code of
conduct: https://www.python.org/psf/codeofconduct/
