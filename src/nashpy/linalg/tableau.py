import warnings
import numpy as np
import numpy.typing as npt
from itertools import cycle
from typing import Tuple, Set, List, Iterable

class TableauBuilder(object):
    def __init__(self, payoffs, shifted = False):
        """

        Parameters
        ----------
        payoffs : array
            a tableau corresponding to a vertex of a polytope.
        shifted : bool
            boolean to shift non basic variables to end of tableau
        """
        self._payoffs = payoffs
        self._shifted = shifted


    def make_positive(self):
        if np.min(self._payoffs) <= 0:
            self._payoffs = self._payoffs + abs(np.min(self._payoffs)) + 1
        return self

    def _build_tableau_matrix(self) -> npt.NDArray:
        slack_vars = np.eye(self._payoffs.shape[0])
        m = np.append(self._payoffs, slack_vars, axis=1)
        if self._shifted:
            m = np.roll(m, slack_vars.shape[1], axis=1)
        targets = np.ones((m.shape[0], 1))
        return np.append(m, targets, axis=1)

    def build(self, algorithm="basic"):
        m = self._build_tableau_matrix()
        if algorithm == "basic":
            return Tableau(m)
        elif algorithm == "lex":
            return TableauLex(m)
        raise ValueError("algorithm "+algorithm+" is not known, use 'basic' or 'lex'")

    @staticmethod
    def column(A : npt.NDArray):
        tb = TableauBuilder(A, shifted=True)
        return tb

    @staticmethod
    def row(B : npt.NDArray):
        tb = TableauBuilder(B.transpose())
        return tb



class Tableau(object):
    def __init__(self, tableau: npt.NDArray, original_basic_labels: Iterable = None):
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
        set
            All lables
        """
        h, w = self._tableau.shape
        real_w = w - h - 1
        return set(range(h + real_w))

    @property
    def non_basic_variables(self) -> Set:
        """
        Identifies the non basic variables of the tableau,
        these correspond to the labels.

        Returns
        -------
        set
            The indices of the non basic variables.
        """

        columns = self._tableau[:, :-1].transpose()
        return set(np.where([np.count_nonzero(col) != 1 for col in columns])[0])

    @property
    def basic_variables(self):
        return self.labels - self.non_basic_variables

    @property
    def slack_variables(self):
        return self.labels - self._original_basic_labels

    def _find_pivot_row(self, column_index: int) -> int:
        row_ratios = self._tableau[:, column_index] / self._tableau[:, -1]
        return np.argmax(row_ratios)

    def _pivot_on_column(self, column_index: int):
        pivot_row_index = self._find_pivot_row(column_index)
        self._pivot(column_index, pivot_row_index)
        return pivot_row_index

    def _pivot(self, column_index: int, pivot_row_index: int):
        for i in range(self._tableau.shape[0]):
            if i != pivot_row_index:
                self._apply_pivot(column_index, pivot_row_index, i)

    def _apply_pivot(self, pivot_col: int, pivot_row: int, applying_row: int):
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
        for i in prev_basic_variables:
            if self._tableau[pivot_row_index, i] != 0:
                return i


    def _extract_label_values(self, column_index: int) -> List:
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
        basic_labels : set
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
    def __init__(self, *kargs, **kwargs):
        self._non_basic_variables = None
        super().__init__(*kargs, **kwargs)

    @property
    def non_basic_variables(self) -> Set:
        if self._non_basic_variables is None:
            self._non_basic_variables = super().non_basic_variables
        return set(self._non_basic_variables)

    def _find_pivot_row(self, column_index: int) -> int:
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
            return np.argmax(row_ratios)

    def _tie_break_lex(self, column_index: int, ties: npt.NDArray) -> int:
        """
        Provides tie breaks if minratio algorithm yields multiple rows. The tiebreaking looks at a perturbed
        problem similar to https://people.math.carleton.ca/~kcheung/math/notes/MATH5801/05/5_3_perturb.html.

        As tableau[:, slack_vars] started out as identity matrix then tableau[:, slack_vars] * e = e
        tableau[:, slack_vars] * e should still reflect how pertubations were alterted through the pivoting matrix operations.
        to tie break we apply minratio test on the pertubed problem. Rather than setting a value for the error, we simply
        rely on error << min(tableau) so we can lexiographically compare entries in tableau
        """
        errs = self._tableau[:, sorted(self.slack_variables)]
        pivot_column = self._tableau[:, (column_index, )]
        err_ratios = errs / pivot_column
        err_ratios[np.isnan(err_ratios)] = -np.inf
        err_ratios[ties == False, :] = -np.inf
        return self._row_sort_asc(err_ratios)[-1]

    def _row_sort_asc(self, m: npt.NDArray) -> npt.NDArray:
        """
        Sorts the rows in m in ascending order, starting with comparing 0th then 1st column
        """
        return np.lexsort(np.flipud(m.transpose()))


    def pivot_and_drop_label(self, column_index: int) -> int:
        """
        In addition to normal tableau logic, ensures entering and leaving labels are recorded

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
