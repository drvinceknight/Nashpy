"""
Tests for the moran process
"""

import numpy as np
import pytest

from hypothesis import given
from hypothesis.extra.numpy import arrays

from nashpy.egt.moran_process import (
    fixation_probabilities,
    get_complete_graph_adjacency_matrix,
    is_population_not_fixed,
    moran_process,
    score_all_individuals,
    update_population,
)


def test_get_complete_graph_adjacency_matrix():
    population = (0, 0, 0, 1, 1, 1, 1)
    adjacency_matrix = get_complete_graph_adjacency_matrix(population=population)
    expected_adjacency_matrix = np.array(
        (
            (0, 1, 1, 1, 1, 1, 1),
            (1, 0, 1, 1, 1, 1, 1),
            (1, 1, 0, 1, 1, 1, 1),
            (1, 1, 1, 0, 1, 1, 1),
            (1, 1, 1, 1, 0, 1, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 1, 0),
        )
    )
    assert np.array_equal(adjacency_matrix, expected_adjacency_matrix)


def test_score_all_individuals_in_3_by_3_game():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    expected_scores = np.array((18, 18, 18, 15, 15, 23, 23))
    scores = score_all_individuals(A=A, population=population)
    assert np.array_equal(expected_scores, scores)


def test_score_all_individuals_in_3_by_3_game_on_cycle():
    """
    Confirm that in this game, each player interacts with a player of the "next"
    time.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    population = np.array((0, 1, 2))
    interaction_graph_adjacency_matrix = np.array(((0, 1, 0), (0, 0, 1), (1, 0, 0)))
    scores = score_all_individuals(
        A=A,
        population=population,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
    )
    expected_scores = np.array((3, 5, 6))
    assert np.array_equal(expected_scores, scores)


def test_score_all_individuals_in_3_by_3_game_on_disconnected_graph():
    """
    Confirm that in this game, each player interacts with no other players. The
    expected scores should be 0.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    population = np.array((0, 1, 2))
    interaction_graph_adjacency_matrix = np.array(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
    scores = score_all_individuals(
        A=A,
        population=population,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
    )
    expected_scores = np.array((0, 0, 0))
    assert np.array_equal(expected_scores, scores)


@given(interaction_graph_adjacency_matrix=arrays(np.bool_, (6, 6)))
def test_properties_of_scores_for_arbitrary_adjacency_matrix(
    interaction_graph_adjacency_matrix,
):
    """
    Confirm that output works and falls within expected bounds for any valid
    interaction_graph.

    Note this uses a strategy that generates a boolean array. However this will
    be considered like a binary array.

    Parameters
    ----------
    interaction_graph_adjacency_matrix : array
        the adjacency matrix for the interaction graph G: individuals of type i
        interact with individuals of type j count towards fitness iff G_{ij} =
        1.  Default is None: if so a complete graph is used -- this corresponds
        to all individuals interacting with each other (with no self
        interactions)
    """
    population = np.array((0, 0, 1, 1, 2, 2))
    M = np.array(((0, 1, 2), (2, 0, 1), (1, 2, 0)))
    scores = score_all_individuals(
        A=M,
        population=population,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
    )
    assert np.min(scores) >= 0
    assert np.max(scores) <= np.sum(M)
    assert len(scores) == len(population)


@given(M=arrays(np.int8, (3, 3), unique=True))
def test_properties_of_scores(M):
    """
    Checks that if non negative valued matrices are passed then non negative
    valued scores are calculated.

    Parameters
    ----------
    M : array
        a payoff matrix
    """
    if np.min(M) >= 0:
        population = np.array((0, 0, 1, 1, 2, 2))
        scores = score_all_individuals(A=M, population=population)
        assert np.min(scores) >= 0
        assert np.sum(scores) > 0
        assert len(scores) == len(population)
    else:
        with pytest.raises(ValueError):
            initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
            tuple(moran_process(A=M, initial_population=initial_population))


def test_update_population_seed_0():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))
    original_set_of_strategies = set(population)

    np.random.seed(0)
    new_population = update_population(
        population=population,
        scores=scores,
        original_set_of_strategies=original_set_of_strategies,
    )
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_seed_1():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 1, 1, 2, 2))
    original_set_of_strategies = set(population)

    np.random.seed(1)
    new_population = update_population(
        population=population,
        scores=scores,
        original_set_of_strategies=original_set_of_strategies,
    )
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_seed_2():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))
    original_set_of_strategies = set(population)

    np.random.seed(2)
    new_population = update_population(
        population=population,
        scores=scores,
        original_set_of_strategies=original_set_of_strategies,
    )
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_with_mutation_probability_1_seed_2():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    mutation_probability = 1
    expected_new_population = np.array((0, 0, 0, 1, 1, 2, 2))
    original_set_of_strategies = set(population)

    np.random.seed(2)
    new_population = update_population(
        population=population,
        scores=scores,
        mutation_probability=mutation_probability,
        original_set_of_strategies=original_set_of_strategies,
    )
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_with_uniform_population():
    population = np.array((0, 0, 0, 0, 0, 0, 0))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    expected_new_population = np.array((0, 0, 0, 0, 0, 0, 0))
    original_set_of_strategies = set(population)

    new_population = update_population(
        population=population,
        scores=scores,
        original_set_of_strategies=original_set_of_strategies,
    )
    assert np.array_equal(expected_new_population, new_population)


def test_update_population_with_identity_replacement_stochastic_matrix():
    """
    With the identity replacement graph as the identity matrix it is not
    possible for the population to change.
    """
    population = np.array((0, 1, 2))
    scores = np.array((18, 15, 23))
    original_set_of_strategies = set(population)
    replacement_stochastic_matrix = np.identity(n=3)

    new_population = update_population(
        population=population,
        scores=scores,
        original_set_of_strategies=original_set_of_strategies,
        replacement_stochastic_matrix=replacement_stochastic_matrix,
    )
    assert np.array_equal(population, new_population)


def test_update_population_with_specific_graph():
    """
    The graph chosen ensures that individuals from the first  three nodes can only
    replace elements at the 4th and 5th nodes.

    The scores ensure this is the only replacement that will happen.

    The various seeds chosen ensure various possibilities are captured.
    """
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    original_set_of_strategies = set(population)
    scores = np.array((18, 18, 18, 0, 0, 0, 0))
    # TODO Fix the dimension of the stochastic matrix
    replacement_stochastic_matrix = np.array(
        (
            (0, 0, 0, 1 / 2, 1 / 2, 0, 0),
            (0, 0, 0, 1 / 2, 1 / 2, 0, 0),
            (0, 0, 0, 1 / 2, 1 / 2, 0, 0),
            (0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 0, 1, 0, 0),
            (0, 0, 0, 0, 0, 1, 0),
            (0, 0, 0, 0, 0, 0, 1),
        )
    )
    expected_new_populations = (
        np.array((0, 0, 0, 1, 0, 2, 2)),
        np.array((0, 0, 0, 0, 1, 2, 2)),
    )
    seeds = (0, 2)

    for seed, expected_new_population in zip(seeds, expected_new_populations):
        np.random.seed(seed)
        new_population = update_population(
            population=population,
            scores=scores,
            original_set_of_strategies=original_set_of_strategies,
            replacement_stochastic_matrix=replacement_stochastic_matrix,
        )
    assert np.array_equal(new_population, expected_new_population)


def test_is_population_not_fixed_for_fixed_population():
    population = np.array((0, 0, 1, 1))
    population_components = ({0, 1}, {2, 3})
    assert (
        is_population_not_fixed(
            population=population, population_components=population_components
        )
        is False
    )


def test_is_population_not_fixed_for_not_fixed_population():
    population = np.array((0, 0, 1, 2))
    population_components = ({0, 1}, {2, 3})
    assert (
        is_population_not_fixed(
            population=population, population_components=population_components
        )
        is True
    )


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
    if np.min(M) >= 0:
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


def test_specific_moran_process_to_effect_of_interaction_graph_seed_0():
    """
    Two subsequent seeded Moran Processes are run.

    In the second we modify the Moran process so that the fixed population type
    no longer interacts.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 1, 2))
    interaction_graph_adjacency_matrix = np.array(((0, 1, 0), (0, 0, 1), (1, 0, 0)))
    np.random.seed(0)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
            interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((2, 2, 2))
    assert np.array_equal(last_generation, expected_last_generation)

    initial_population = np.array((0, 1, 2))
    interaction_graph_adjacency_matrix = np.array(((0, 1, 0), (0, 0, 1), (0, 0, 0)))
    np.random.seed(0)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
            interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 0))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_for_effect_of_replacement_stochastic_matrix_seed_0():
    """
    Two subsequent seeded Moran Processes are run.

    In the second we modify the Moran process so that the fixed population type
    no longer replaces anyone but itself.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 1, 2))
    np.random.seed(0)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((2, 2, 2))
    assert np.array_equal(last_generation, expected_last_generation)

    initial_population = np.array((0, 1, 2))
    replacement_stochastic_matrix = np.array(
        (
            (1 / 3, 1 / 3, 1 / 3),
            (1 / 3, 1 / 3, 1 / 3),
            (0, 0, 1),
        )
    )
    np.random.seed(0)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
            replacement_stochastic_matrix=replacement_stochastic_matrix,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 0))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_for_effect_of_replacement_stochastic_matrix_seed_1():
    """
    Two subsequent seeded Moran Processes are run.

    In the first there is no replacement matrix: the population fixes with a
    single type.
    In the second the replacement matrix represents a partitioned population.
    The population fixes with two types.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 1, 2, 1))
    np.random.seed(1)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((1, 1, 1, 1))
    assert np.array_equal(last_generation, expected_last_generation)

    initial_population = np.array((0, 1, 2, 1))
    replacement_stochastic_matrix = np.array(
        (
            (1 / 2, 1 / 2, 0, 0),
            (1 / 2, 1 / 2, 0, 0),
            (0, 0, 1 / 2, 1 / 2),
            (0, 0, 1 / 2, 1 / 2),
        )
    )
    np.random.seed(1)
    generations = tuple(
        moran_process(
            A=A,
            initial_population=initial_population,
            replacement_stochastic_matrix=replacement_stochastic_matrix,
        )
    )
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 2, 2))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_seed_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(1)
    generations = tuple(moran_process(A=A, initial_population=initial_population))
    last_generation = generations[-1]
    expected_last_generation = np.array((2, 2, 2, 2, 2, 2, 2))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_with_mutation_seed_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    mutation_probability = 0.2
    np.random.seed(0)
    generator = moran_process(
        A=A,
        initial_population=initial_population,
        mutation_probability=mutation_probability,
    )
    generations = [next(generator) for _ in range(10)]
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 0, 1, 1, 0, 0))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_with_mutation_seed_0_mutation_probability_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    mutation_probability = 1
    np.random.seed(0)
    generator = moran_process(
        A=A,
        initial_population=initial_population,
        mutation_probability=mutation_probability,
    )
    generations = [next(generator) for _ in range(10)]
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 2, 1, 1, 1, 1))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_with_mutation_seed_2():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    mutation_probability = 0.2
    np.random.seed(2)
    generator = moran_process(
        A=A,
        initial_population=initial_population,
        mutation_probability=mutation_probability,
    )
    generations = [next(generator) for _ in range(10)]
    last_generation = generations[-1]
    expected_last_generation = np.array((0, 0, 2, 1, 1, 1, 0))
    assert np.array_equal(last_generation, expected_last_generation)


def test_specific_moran_process_with_mutation_seed_3():
    """
    This is a test for an example in the discussion documentation BUT also
    checks a specific seed where a bug existed regarding the selection
    probabilities with a 0 value in the payoff matrix during mutation.
    """
    A = np.array([[2, 1], [3, 0]])
    initial_population = [0, 0, 0, 0, 1]
    mutation_probability = 0.2
    seed = 6
    np.random.seed(seed)
    generator = moran_process(
        A=A,
        initial_population=initial_population,
        mutation_probability=mutation_probability,
    )
    generations = [next(generator) for _ in range(10)]
    last_generation = generations[-1]
    expected_last_generation = np.array((1, 0, 1, 1, 1))
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
    expected_probabilities = {
        (0, 0, 0, 0, 0, 0, 0): 0.5,
        (1, 1, 1, 1, 1, 1, 1): 0.3,
        (2, 2, 2, 2, 2, 2, 2): 0.2,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = {
        (0, 0, 0, 0, 0, 0, 0): 0.2,
        (1, 1, 1, 1, 1, 1, 1): 0.3,
        (2, 2, 2, 2, 2, 2, 2): 0.5,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_with_fixed_initial_population_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 0))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = {
        (0, 0, 0, 0): 1,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_with_fixed_initial_population_2():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((2, 2, 2, 2, 2, 2))
    np.random.seed(1)
    repetitions = 10
    probabilities = fixation_probabilities(
        A=A, initial_population=initial_population, repetitions=repetitions
    )
    expected_probabilities = {
        (2, 2, 2, 2, 2, 2): 1,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_on_graphs_0():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(0)
    repetitions = 10
    interaction_graph_adjacency_matrix = np.array(
        (
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 0, 1, 1, 1),
            (0, 1, 0, 0, 1, 0, 1),
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (0, 1, 1, 1, 1, 1, 1),
        )
    )
    replacement_stochastic_matrix = np.array(
        (
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (0, 0, 0, 1 / 3, 1 / 3, 1 / 3, 0),
            (0, 0, 0, 1 / 3, 1 / 3, 1 / 3, 0),
            (0, 0, 0, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (0, 0, 0, 0, 0, 1 / 2, 1 / 2),
        )
    )
    probabilities = fixation_probabilities(
        A=A,
        initial_population=initial_population,
        repetitions=repetitions,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
        replacement_stochastic_matrix=replacement_stochastic_matrix,
    )

    expected_probabilities = {
        (0, 0, 0, 1, 1, 1, 1): 0.2,
        (0, 0, 0, 2, 2, 2, 2): 0.8,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_on_graphs_1():
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 0, 0, 1, 1, 2, 2))
    np.random.seed(1)
    repetitions = 10
    interaction_graph_adjacency_matrix = np.array(
        (
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 0, 1, 1, 1),
            (0, 1, 0, 0, 1, 0, 1),
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (0, 1, 1, 1, 1, 1, 1),
        )
    )
    replacement_stochastic_matrix = np.array(
        (
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (1 / 3, 1 / 3, 1 / 3, 0, 0, 0, 0),
            (0, 0, 0, 1 / 3, 1 / 3, 1 / 3, 0),
            (0, 0, 0, 1 / 3, 1 / 3, 1 / 3, 0),
            (0, 0, 0, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (0, 0, 0, 0, 0, 1 / 2, 1 / 2),
        )
    )
    probabilities = fixation_probabilities(
        A=A,
        initial_population=initial_population,
        repetitions=repetitions,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
        replacement_stochastic_matrix=replacement_stochastic_matrix,
    )

    expected_probabilities = {
        (0, 0, 0, 1, 1, 1, 1): 0.3,
        (0, 0, 0, 2, 2, 2, 2): 0.7,
    }
    assert probabilities == expected_probabilities


def test_fixation_probablities_with_initial_fixed_population_on_graphs_0():
    """
    The replacement graph is completely disconnected so the initial population
    is fixed.
    """
    A = np.array(((4, 3, 2), (1, 2, 5), (6, 1, 3)))
    initial_population = np.array((0, 1, 0, 1, 2, 0, 2))
    np.random.seed(0)
    repetitions = 10
    interaction_graph_adjacency_matrix = np.array(
        (
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 0, 1, 1, 1),
            (0, 1, 0, 0, 1, 0, 1),
            (0, 1, 1, 0, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (1, 1, 1, 1, 1, 0, 1),
            (0, 1, 1, 1, 1, 1, 1),
        )
    )
    replacement_stochastic_matrix = np.identity(7)
    probabilities = fixation_probabilities(
        A=A,
        initial_population=initial_population,
        repetitions=repetitions,
        interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
        replacement_stochastic_matrix=replacement_stochastic_matrix,
    )

    expected_probabilities = {
        (0, 1, 0, 1, 2, 0, 2): 1,
    }
    assert probabilities == expected_probabilities
