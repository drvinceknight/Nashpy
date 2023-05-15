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
    def non_basic_variables(self):
        if self._non_basic_variables is None:
            self._non_basic_variables = super().non_basic_variables
        return set(self._non_basic_variables)

    def _find_pivot_row_old(self, column_index: int) -> int:
        """
        First applies normal tableau logic to find the pivot row.
        The implied size of the pertubation matrix is used to break any ties
        """
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                r"invalid value encountered in true_divide|divide by zero encountered in true_divide",
            )

            Cq = self._tableau[:, -1]
            self._tableau[:, sorted(self.slack_variables)]
            #C = self._tableau[:, sorted(self.slack_variables)] / np.reshape(Cq, (Cq.shape[0], 1))
            #C[np.isnan(C)] = np.inf
            lex_order_reversed = np.lexsort(np.rot90(C))
            lex_order = -lex_order_reversed + lex_order_reversed.shape[0]

            # gets ratio of each row
            pivot_column = self._tableau[:, column_index]
            Cq = self._tableau[:, -1]

            # catch divide by zero warning

            ratio = np.divide(Cq, pivot_column)
            #ratio[np.isnan(ratio)] = np.inf

        # filters for column coefficients <=0 (to preserve feasibility)
        filtered_ratio = np.where(pivot_column <= 0, np.full(ratio.shape, np.inf), ratio)

        return np.lexsort(np.flipud((filtered_ratio, lex_order)))[0]

    def _find_pivot_row(self, column_index: int) -> int:
        pertubations = self._tableau[:, sorted(self.slack_variables)]
        errors = np.power(1e-7, np.arange(pertubations.shape[0]))
        errors = np.reshape(errors, (errors.size, 1))
        calc_errs = pertubations.dot(errors)

        row_ratios = self._tableau[:, column_index] / self._tableau[:, -1]
        row_ratios[np.isnan(row_ratios)] = -np.inf
        ties = row_ratios == np.max(row_ratios)
        if sum(ties) > 1:
            row_ratios = calc_errs[:,0] / self._tableau[:, column_index]
            row_ratios[np.isnan(row_ratios)] = -np.inf
            row_ratios[ties == False] = -np.inf

            #print("Tie: ", row_ratios)

        return np.argmax(row_ratios)



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
