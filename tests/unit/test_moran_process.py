"""
Tests for the moran process
"""
import numpy as np

from nashpy.egt.moran_process import (
    score_all_individuals,
    update_population,
    moran_process,
)


def test_score_all_individuals_in_3_by_3_game():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    expected_scores = np.array((18, 18, 18, 15, 15, 23, 23))
    scores = score_all_individuals(A=A, population=population)
    assert np.array_equal(expected_scores, scores)


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


def test_moran_process_in_3_by_3_game():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
