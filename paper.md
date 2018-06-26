---
title: 'Nashpy: A Python library for the computation of Nash equilibria'
tags:
  - Python
  - mathematics
  - economics
  - computer science
  - game theory
  - equilibrium
authors:
  - name: Vincent Knight
    orcid: 0000-0002-4245-0638
    affiliation: 1
  - name: James Campbell
    orcid: 0000-0003-1100-1765
    affiliation: 1
affiliations:
 - name: Cardiff University, School of Mathematics, UK
   index: 1
date: 13 August 2018
bibliography: paper.bib
---

# Summary

Game theory is the study of strategic interactions where the outcomes of choice
depend on the choices of all participants. A key solution concept in the field
is that of Nash Equilibrium [@nash1950equilibrium]. This solution concept
corresponds to a coordinate at which no participant has any incentive to change
their choice. Some applications of this concept include the modelling of
healthcare decisions [@knight2017measuring] as well as evolutionary game theory.
A number of algorithms exist to compute this Nash equilibria, for example the
Lemke-Howson algorithm [@lemke1964equilibrium].

The state of the art in terms of software implementations of these algorithms
is **Gambit** [@mckelvey2006gambit]. Gambit includes a python wrapper to its
core C functionality however is not currently portable (for example
Windows is not supported).

``Nashpy`` is a Python library with all dependencies being part of the standard
scientific Python stack (numpy and scipy [@scipy]) thus it is portable. Nashpy
currently implements 3 algorithms for the computation of equilibria (currently
only for 2 player games) and is extensively documented, including theoretic
reference material on the algorithms:
[nashpy.readthedocs.io](http://nashpy.readthedocs.io/). This documentation
coupled with the readability of Python make it a particularly effective teaching
tool as students can inspect the code to reinforce
their understanding of the algorthms.
Furthermore, the
software is automatically tested using a combination of unit, integration and
property based tests with 100% coverage. All the documentation is doctested and
in fact the example in this paper is as well.

Here is an example of how to use ``Nashpy`` to obtain the
equilibria for a game with 2 pure and 1 mixed equilibria:

```
>>> import nashpy as nash
>>> import numpy as np
>>> A = np.array([[2, 0], [0, 1]])
>>> B = np.array([[1, 0], [0, 2]])
>>> game = nash.Game(A, B)
>>> for eq in game.support_enumeration():
...     print(eq)
(array([ 1.,  0.]), array([ 1.,  0.]))
(array([ 0.,  1.]), array([ 0.,  1.]))
(array([ 0.666...,  0.333...]), array([ 0.333...,  0.666...]))

```

``Nashpy`` is designed to be used by researchers and students in courses in the
fields of mathematics, computer science and/or economics. It is already
currently being used in a final year course at Cardiff University.
``Nashpy`` has been archived to Zenodo with the linkd DOI:
[@zenodo].


```

# Acknowledgements

We acknowledge code contributions from Ria Baldevia as well as many helpful
discussions with Nikoleta Glynatsi.

# References
