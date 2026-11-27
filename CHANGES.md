# Unreleased

Replace the fixed learning-rate update in `Game.regret_minimization` with
cumulative regret matching and fix column payoffs in rectangular games. The
generator now yields the average mixed strategies played across all rounds.
Existing calls that supply a numeric `learning_rate` still work and emit a
deprecation warning. Use `iterations=` to set the number of rounds.

Fix imitation dynamics for rectangular games and correct the column player's
payoff calculation. Imitation dynamics now uses a local NumPy random number
generator and accepts `seed=0`. Use `seed=` in place of `random_seed=`.
The same seed can produce different results than in v0.0.43 because of the
new generator and bug fixes.

Handle players with only one available action in introspection dynamics.

Avoid exponential overflow and underflow in stochastic fictitious play without
rescaling payoffs or changing the logit parameter.

# v0.0.43

Fix errors in introspection documentation.

# v0.0.42

Add introspection dynamics.

# v0.0.41

Add exercises to a number of text book chapters.

# v0.0.40

Add more documentation on Zero sum games.

# v0.0.39

Implement linear program for Zero sum games.

# v0.0.38

Fix a bug in stochastic fictitious play.

# v0.0.37

Implementation of moran processes on graphs.

# v0.0.36

Reorganisation of docs.

# v0.0.35

Addition to the documentation.

# v0.0.34

Documentation improvements and allow for zero values in Moran process.

# v0.0.33

Documentation improvements and add replicator-mutator equation.

# v0.0.32

Fix lower bound for numpy in setup configuration.

# v0.0.31

Add fixation with mutation.

# v0.0.30

Fix an error in the docs for the repeated games.

# v0.0.29

Add ability to create new games as repeated games.

# v0.0.28

Modify fixation probability api.

# v0.0.27

Add fixation probability calculation.

# v0.0.26

Add Moran process

# v0.0.25

Fix a bug in the documentation.

# v0.0.24

Add best response check functionality, a large amount of documentation and some
CI improvements.

# v0.0.23

A number of build improvements and fixes.

# v0.0.22

Add asymmetric replicator dynamics.

# v0.0.21

Add stochastic fictitious play.

# v0.0.20

Add replicator dynamics.

# v0.0.19

Add fictitious play learning algorithm and support for py3.7

# v0.0.18

Minor edits and final version of JOSS paper.

# v0.0.17

Minor edit to documentation.

# v0.0.16

Minor edit to documentation.

# v0.0.15

Add support for degenerate games in support enumeration.

# v0.0.14

Change module name to `nashpy`. Now for consistency have:

`$ pip install nashpy`

and

`>>> import nashpy`

# v0.0.13

Add a warning for nonsensical output from lemke-howson.

# v0.0.12

Add another game theoretic library to documentation.

# v0.0.11

Very minor documentation fix.

# v0.0.10

Add enumeration method for the Lemke Howson algorithm as well as a more
extensive reference document.

# v0.0.9

Add implementation of the Lemke Howson algorithm

# v0.0.8

Add discussion section to documentation

# v0.0.7

Documentation

# v0.0.6

Add vertex enumeration algorithm.

# v0.0.5

Add ability to calculate utilities against a given pair of strategies.

# v0.0.4

Unpin numpy version number for easier installation.

# v0.0.3

Various packaging and testing improvements and a CITATION.md file.

# v0.0.2

Fix bug for pip installing.

# v0.0.1

First release
