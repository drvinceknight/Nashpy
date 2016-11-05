# Nash: a python library for the computation of equilibria of normal form games.

**This is a library with standard dependencies so that it is pip installable: if
you want to do sophisticated equilibria computation you should use
[gambit](https://github.com/gambitproject/gambit).**

This code is based on code that was implemented in
[Sagemath](http://www.sagemath.org/).

## Installation

The easiest way to install is from pypi:

```bash
$ pip install nashpy  # This doesn't work yet  #TODO Speak to James
```

## Usage

You can create a zero sum game:

```python
>>> import nash
>>> A = [[1, -1], [-1, 1]]
>>> matching_pennies = nash.Game(A)
>>> matching_pennies.zero_sum
True

```

To compute the equilibria you can iterate over `Game.equilibria()` which is a
generator:

```python
>>> for eq in matching_pennies.equilibria():
...     print(eq)
(array([ 0.5,  0.5]), array([ 0.5,  0.5]))

```

You can also create bi matrix games:

```python
>>> A = [[1, 2], [3, 0]]
>>> B = [[0, 2], [3, 1]]
>>> battle_of_the_sexes = nash.Game(A, B)
>>> battle_of_the_sexes.zero_sum
False
>>> for eq in battle_of_the_sexes.equilibria():
...     print(eq)
(array([ 1.,  0.]), array([ 0.,  1.]))
(array([ 0.,  1.]), array([ 1.,  0.]))
(array([ 0.5,  0.5]), array([ 0.5,  0.5]))

```


## Development

To run the full test suite:

```
$ python setup.py test
```
