"""
Tests for the moran process
"""
import numpy as np
import pytest

from hypothesis import given
from hypothesis.extra.numpy import arrays

from nashpy.egt.moran_process import (
    score_all_individuals,
    update_population,
    moran_process,
    fixation_probabilities,
)


def test_score_all_individuals_in_3_by_3_game():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    expected_scores = np.array((18, 18, 18, 15, 15, 23, 23))
    scores = score_all_individuals(A=A, population=population)
    assert np.array_equal(expected_scores, scores)


@given(M=arrays(np.int8, (3, 3), unique=True))
def test_properties_of_scores(M):
    """
    Checks that if non negative valued matrices are passed then non negative
    valued scored are calculated.

    Parameters
    ----------
    M : array
        a payoff matrix
    """
    if np.min(M) > 0:
        population = np.array((0, 0, 1, 1, 2, 2))
        scores = score_all_individuals(A=M, population=population)
        assert np.min(scores) >= 0
        assert np.sum(scores) > 0
    else:
        with pytest.raises(ValueError):
            initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
            tuple(moran_process(A=M, initial_population=initial_population))


def test_update_population_seed_0():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))

    np.random.seed(0)
    new_population = update_population(population=population, scores=scores)
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_seed_1():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 1, 1, 2, 2))

    np.random.seed(1)
    new_population = update_population(population=population, scores=scores)
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_with_uniform_population():
    population = np.array((0, 0, 0, 0, 0, 0, 0))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 0, 0, 0, 0))

    new_population = update_population(population=population, scores=scores)
    assert np.array_equal(expected_new_population, new_population)


@given(M=arrays(np.int8, (3, 3), unique=True))
def test_moran_process_in_3_by_3_game(M):
    """
    This tests that the final population only has a single population in it and
    that all generations have a population of the correct length and the correct
    possible entries.

    Note that only non negative sampled matrices are used for tests.

    Parameters
    ----------
    M : array
        a payoff matrix
    """
    if np.min(M) > 0:
        initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
        generations = tuple(moran_process(A=M, initial_population=initial_population))
        last_generation = generations[-1]
        assert set(map(len, generations)) == {len(initial_population)}
        assert all(set(population) <= {0, 1, 2} for population in generations)
        assert set(last_generation) in ({0}, {1}, {2})
    else:
        with pytest.raises(ValueError):
            initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
            tuple(moran_process(A=M, initial_population=initial_population))


def test_specific_moran_process_seed_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(0)
    generations = tuple(moran_process(A=A, initial_population=initial_population))
    last_generation = generations[-1]
    expected_last_generation = np.array((1, 1, 1, 1, 1, 1, 1))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_seed_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(1)
    generations = tuple(moran_process(A=A, initial_population=initial_population))
    last_generation = generations[-1]
    expected_last_generation = np.array((2, 2, 2, 2, 2, 2, 2))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_with_already_fixed_initial_population():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0))
    generations = tuple(moran_process(A=A, initial_population=initial_population))
    assert len(generations) == 1
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 0))
    assert np.array_equal(last_generation, expected_last_generation)


def test_fixation_probablities_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(0)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = np.array((0.5, 0.3, 0.2))
    assert np.allclose(probabilities, expected_probabilities)


def test_fixation_probablities_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = np.array((0.2, 0.3, 0.5))
    assert np.allclose(probabilities, expected_probabilities)


def test_fixation_probablities_with_fixed_initial_population_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 0))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = np.array((1, 0, 0))
    assert np.array_equal(probabilities, expected_probabilities)


def test_fixation_probablities_with_fixed_initial_population_2():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((2, 2, 2, 2, 2, 2))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = np.array((0, 0, 1))
    assert np.array_equal(probabilities, expected_probabilities)
