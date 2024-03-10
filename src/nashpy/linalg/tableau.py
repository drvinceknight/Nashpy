"""A class for the tableaus used in the Lemke Howson algorithms"""

import warnings
import numpy as np
import numpy.typing as npt
from typing import Set, List, Iterable, Optional


def create_row_tableau(payoffs: npt.NDArray, lexicographic=True):
    """
    Creates a row tableau

    Parameters
    ----------
    payoffs : array
        The payoff matrix, typically for column (B) player
    lexicographic : bool
        Whether the tableau should use lex sorting to handle degenerate games
    Returns
    -------
    Tableau
        The corresponding row tableau for the payoff matrix
    """
    tableau = _build_tableau_matrix(payoffs.transpose(), False)
    if lexicographic:
        return TableauLex(tableau)
    return Tableau(tableau)


def create_col_tableau(payoffs: npt.NDArray, lexicographic=False):
    """
    Creates a column tableau

    Parameters
    ----------
    payoffs : array
        The payoff matrix, typically for row (A) player
    lexicographic : bool
        Whether the tableau should use lex sorting to handle degenerate games
    Returns
    -------
    Tableau
        The corresponding column tableau for the payoff matrix
    """
    tableau = _build_tableau_matrix(payoffs, True)
    if lexicographic:
        return TableauLex(tableau)
    return Tableau(tableau)


def _build_tableau_matrix(payoffs: npt.NDArray, shifted: bool) -> npt.NDArray:
    """
    Build the tableau matrix from payoff. Can be shifted to preserve label indices.
    As required in lemke howson, payoffs are ensured to be positive.
    Adding a constant would anyways never affect the equilibrium

    Parameters
    ----------
    payoffs : array
        The payoff matrix
    shifted : bool
        When True, first indices will be slack vars

    Returns
    -------
    array
        the tableau matrix
    """
    if np.min(payoffs) <= 0:
        payoffs = payoffs + abs(np.min(payoffs)) + 1
    slack_vars = np.eye(payoffs.shape[0])
    targets = np.ones((payoffs.shape[0], 1))
    if shifted:
        return np.concatenate([slack_vars, payoffs, targets], axis=1)
    return np.concatenate([payoffs, slack_vars, targets], axis=1)


class Tableau(object):
    """
    An implementation of a standard Tableau
    Tableaus are well known in linear optimizations
    problems and e.g. part of the simplex algorithm.
    """

    def __init__(
        self, tableau: npt.NDArray, original_basic_labels: Optional[Iterable] = None
    ):
        """
        Constructs a Tableau for solving lemke-howson algorithm.

        Parameters
        ----------
        tableau : array
            The tableau off a payoff matrix
        original_basic_labels : Optional[Iterable]
            By default this corresponds to the non-basic variables.
            There should be no need to override this unless tableau
            matrix was manipulated prior to calling constructor
        """
        self._tableau = tableau
        if original_basic_labels is not None:
            self._original_basic_labels = set(original_basic_labels)
        else:
            self._original_basic_labels = self.non_basic_variables

    @property
    def labels(self) -> Set:
        """
        The full set of labels

        Returns
        -------
        Set
            All lables
        """
        h, w = self._tableau.shape
        real_w = w - h - 1
        return set(range(h + real_w))

    @property
    def non_basic_variables(self) -> Set:
        """
        Identifies the non basic variables of the tableau,
        these correspond to the basic labels.

        Returns
        -------
        Set
            The indices of the non basic variables.
        """

        columns = self._tableau[:, :-1].transpose()
        return set(np.where([np.count_nonzero(col) != 1 for col in columns])[0])

    @property
    def basic_variables(self) -> Set:
        """
        Identifies the basic variables of the tableau
        these correspond to the non-basic labels

        Returns
        -------
        Set
            The indices of the basic variables.
        """
        return self.labels - self.non_basic_variables

    @property
    def slack_variables(self) -> Set:
        """
        Identifies the slack variables of the tableau
        These were the original non-basic labels when
        tableau was generated and should not change over time

        Returns
        -------
        Set
            The indices of the slack variables
        """
        return self.labels - self._original_basic_labels

    def _find_pivot_row(self, column_index: int) -> int:
        """
        Uses minratio test to find the row to pivot against.
        To avoid divide-by-zeros this is implemented using max ratio

        Parameters
        ----------
        column_index : int
            The column/label to pivot.

        Returns
        -------
        int
            The row to pivot against
        """
        row_ratios = self._tableau[:, column_index] / self._tableau[:, -1]
        return int(np.argmax(row_ratios))

    def _pivot_on_column(self, column_index: int):
        """
        Perform a column pivot, returning the row/dropped label

        Parameters
        ----------
        column_index : int
            The column/label to pivot.

        Returns
        -------
        int
            The row chosen to pivot against
        """
        pivot_row_index = self._find_pivot_row(column_index)
        self._pivot(column_index, pivot_row_index)
        return pivot_row_index

    def _pivot(self, column_index: int, pivot_row_index: int):
        """
        Perform row operations to drop column from all but the pivot row

        Parameters
        ----------
        column_index : int
            The column/label to pivot.
        pivot_row_index : int
            The row to pivot
        """
        for i in range(self._tableau.shape[0]):
            if i != pivot_row_index:
                self._apply_pivot(column_index, pivot_row_index, i)

    def _apply_pivot(self, pivot_col: int, pivot_row: int, applying_row: int):
        """
        Dropping pivot value on the applying row

        Parameters
        ----------
        pivot_col : int
            The column/label to pivot.
        pivot_row : int
            The row to pivot
        applying_row : int
            The row to drop pivot column from
        """
        pivot_element = self._tableau[pivot_row, pivot_col]
        row_pivot_val = self._tableau[applying_row, pivot_col]
        row = self._tableau[applying_row, :] * pivot_element
        row -= self._tableau[pivot_row, :] * row_pivot_val
        self._tableau[applying_row, :] = row

    def pivot_and_drop_label(self, column_index: int) -> int:
        """
        Pivots the tableau and returns the dropped label

        Parameters
        ----------
        column_index : int
            The index of a tableau on which to pivot.

        Returns
        -------
        int
            The dropped label.
        """
        prev_basic_vars = self.basic_variables
        row = self._pivot_on_column(column_index)
        dropped = self._find_dropped(row, prev_basic_vars)
        return dropped

    def _find_dropped(self, pivot_row_index: int, prev_basic_variables: Set) -> int:
        """
        Identifies the dropped label

        Parameters
        ----------
        pivot_row_index : int
            The row to find dropped label from
        prev_basic_variables : Set
            The candidates for labels that might have been dropped

        Returns
        -------
        int
            The dropped label

        Raises
        ------
        ValueError
            if no dropped label is identified.
        """
        for i in prev_basic_variables:
            if self._tableau[pivot_row_index, i] != 0:
                return i
        raise ValueError("could not find dropped label")

    def _extract_label_values(self, column_index: int) -> List:
        """
        Calculates equlibria for a basic label in strategy

        Parameters
        ----------
        column_index : int
            The basic label to compute strategy for

        Returns
        -------
        List
            The computed unnormalized strategy
        """
        vertex = []
        for row, value in zip(self._tableau[:, column_index], self._tableau[:, -1]):
            if row != 0:
                vertex.append(value / row)
        return vertex

    def to_strategy(self, basic_labels: Set) -> npt.NDArray:
        """
        Return a strategy vector from a tableau

        Parameters
        ----------
        basic_labels : Set
            the set of basic labels in the other tableau.

        Returns
        -------
        array
            A strategy.
        """

        vertex = []
        for column in self._original_basic_labels:
            if column in basic_labels:
                vertex += self._extract_label_values(column)
            else:
                vertex.append(0)
        strategy = np.array(vertex)
        return strategy / sum(strategy)


class TableauLex(Tableau):
    """
    A tableau with lexiographic sorting to break ties when pivoting.
    This avoids endless looping that might occur with a standard
    tableau when applied on degenerate games.
    """

    def __init__(self, *kargs, **kwargs):
        """
        Constructs a lex Tableau for solving degenerate games.
        Parameters are inherited from Tableau

        Parameters
        ----------
        *kargs : Any
            Positional arguments passed to Tableau constructor
        **kwargs : Any
            Key value arguments passed to Tableau constructor
        """
        self._non_basic_variables = None
        super().__init__(*kargs, **kwargs)

    @property
    def non_basic_variables(self) -> Set:
        """
        Identifies the non basic variables of the tableau,
        these correspond to the basic labels. For lex algorithm
        a non-basic variable must have been dropped in an earlier pivot

        Returns
        -------
        Set
            The indices of the non basic variables.
        """

        if self._non_basic_variables is None:
            self._non_basic_variables = super().non_basic_variables
        return set(self._non_basic_variables)

    def _find_pivot_row(self, column_index: int) -> int:
        """
        Finding the row to pivot like std tableau, but applying lex sorting to resolve ties in minratio.

        Parameters
        ----------
        column_index : int
            The column/label to pivot.

        Returns
        -------
        int
            The label to drop.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                r"invalid value encountered in true_divide|divide by zero encountered in true_divide",
            )
            row_ratios = self._tableau[:, column_index] / self._tableau[:, -1]
            row_ratios[np.isnan(row_ratios)] = -np.inf
            ties = row_ratios == np.max(row_ratios)
            if sum(ties) > 1:
                return self._tie_break_lex(column_index, ties)
            return int(np.argmax(row_ratios))

    def _tie_break_lex(self, column_index: int, ties: npt.NDArray) -> int:
        """
        Provides tie breaks if minratio algorithm yields multiple rows. The tiebreaking looks at a perturbed
        problem similar to https://people.math.carleton.ca/~kcheung/math/notes/MATH5801/05/5_3_perturb.html.

        As tableau[:, slack_vars] started out as identity matrix then tableau[:, slack_vars] * e = e
        tableau[:, slack_vars] * e should still reflect how pertubations were alterted through the pivoting matrix operations.
        to tie break we apply minratio test on the pertubed problem. Rather than setting a value for the error, we simply
        rely on error << min(tableau) so we can lexiographically compare entries in tableau

        Parameters
        ----------
        column_index : int
            The label to pivot.
        ties: array
            The rows to perform tiebreak on

        Returns
        -------
        int
            The row to pivot on
        """
        errs = self._tableau[:, sorted(self.slack_variables)]
        pivot_column = self._tableau[:, (column_index,)]
        err_ratios = errs / pivot_column
        err_ratios[np.isnan(err_ratios)] = -np.inf
        err_ratios[np.logical_not(ties), :] = -np.inf
        return self._row_sort_asc(err_ratios)[-1]

    def _row_sort_asc(self, m: npt.NDArray) -> npt.NDArray:
        """
        Sorts the rows in m in ascending order, starting with comparing 0th then 1st column

        Parameters
        ----------
        m : array
            The matrix to sort

        Returns
        -------
        array
            The order of the entries
        """
        return np.lexsort(np.flipud(m.transpose()))

    def pivot_and_drop_label(self, column_index: int) -> int:
        """
        In addition to standard tableau logic this ensures entering and leaving labels are recorded

        Parameters
        ----------
        column_index : int
            The index of a tableau on which to pivot.

        Returns
        -------
        int
            The dropped label.
        """
        dropped = super().pivot_and_drop_label(column_index)
        self._non_basic_variables.add(dropped)
        self._non_basic_variables.remove(column_index)
        return dropped
