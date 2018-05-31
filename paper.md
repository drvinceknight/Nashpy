---
title: 'Nashpy: A Python library for the computation of Nash equilibria'
tags:
  - Python
  - mathematics
  - economics
  - computer science
  - game theory
  - equilbrium
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
[nashpy.readthedocs.io](http://nashpy.readthedocs.io/). Furthermore, the
software is automatically tested using a combination of unit, integration and
property based tests with 100% coverage.

``Nashpy`` is designed to be used by researchers and students in courses in the
fields of mathematics, computer science and/or economics. It is already
currently being used in a final year course at Cardiff University.
Due to the fact that the code is written entirely in Python and is open source,
this makes it a positive teaching tool as students can read and understand
implementation of the algorithms.
``Nashpy`` has been archived to Zenodo with the linkd DOI:
[@zenodo].

# Acknowledgements

I acknowledge code contributions from Ria Baldevia as well as many helpful
discussions with Nikoleta Glynatsi.

# References
