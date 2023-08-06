# This file includes code from:
# LINEX webtool
# Copyright (C) 2021  LipiTUM group, Chair of experimental Bioinformatics, Technical University of Munich
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import numpy as np

# From package
from .utils import (
    correlations,
    partial_correlations,
    _matrix_pval_correction_,
    SymmetricMatrix,
    correlation_change,
    fold_changes,
    binary_test,
)
from .exceptions import SignificanceTestError
from .misc import _pandas_log_


def _correlation_computation_(self, attr: str,
                              method: str = "pearson",
                              estimator: str = "LedoitWolf",
                              significance: float = 0.05,
                              overwrite: bool = False,
                              correct_args: dict = None,
                              **kwargs):
    self._check_data_(check_groups=False)
    if self.groups is None:
        if not overwrite:
            if self.interaction_attributes.get(attr) is not None and self.interaction_attributes.get(attr):
                return
        if attr == "correlations":
            cors, pvals = correlations(self.data,
                                       method=method,
                                       **kwargs)
        else:
            cors, pvals = partial_correlations(self.data, estimator,
                                               **kwargs)
        # multiple test correction
        if not (pvals < 0).all():
            if correct_args is None:
                corr_pvals = _matrix_pval_correction_(pvals)
            else:
                corr_pvals = _matrix_pval_correction_(pvals, **correct_args)
            corr_pvals = pd.DataFrame(corr_pvals, cors.index, cors.columns)
            sig_mask = corr_pvals >= significance
            cors.values[sig_mask] = 0
        else:
            corr_pvals = pvals
        self.interaction_attributes[attr] = SymmetricMatrix(cors)
        self.interaction_attributes[f"{attr}_pvals"] = SymmetricMatrix(pd.DataFrame(corr_pvals,
                                                                                    cors.index,
                                                                                    cors.columns))
    else:
        if (self.interaction_attributes.get(attr) is None or
                not self.interaction_attributes.get(attr) or
                overwrite or
                isinstance(self.interaction_attributes.get(attr), SymmetricMatrix)
        ):
            self.interaction_attributes[attr] = {}
            self.interaction_attributes[f"{attr}_pvals"] = {}
            group_correlations = self.unique_groups.size * [False]
        else:
            group_correlations = [self.interaction_attributes[attr].get(group)
                                  is not None for group in self.unique_groups]
            if all(group_correlations):
                return
            elif (self.interaction_attributes.get(f"{attr}_pvals") is None or
                  overwrite or
                  isinstance(self.interaction_attributes.get(f"{attr}_pvals"), SymmetricMatrix)
            ):
                self.interaction_attributes[f"{attr}_pvals"] = {}

        for group in self.unique_groups[np.invert(group_correlations)]:
            group_data = self.data.loc[:, self.groups == group]
            if attr == "correlations":
                cors, pvals = correlations(group_data,
                                           method=method,
                                           **kwargs)
            else:
                cors, pvals = partial_correlations(group_data, estimator,
                                                   **kwargs)
            # multiple test correction
            if not (pvals < 0).all():
                if correct_args is None:
                    corr_pvals = _matrix_pval_correction_(pvals)
                else:
                    corr_pvals = _matrix_pval_correction_(pvals, **correct_args)
                sig_mask = corr_pvals >= significance
                cors.values[sig_mask] = 0
                cors = cors.fillna(0)
            else:
                corr_pvals = pvals
            self.interaction_attributes[attr][group] = SymmetricMatrix(cors)
            self.interaction_attributes[f"{attr}_pvals"][group] = SymmetricMatrix(pd.DataFrame(corr_pvals,
                                                                                               cors.index,
                                                                                               cors.columns))


def compute_correlations(self,
                         method: str = "pearson",
                         significance: float = 0.05,
                         overwrite: bool = False,
                         correct_args: dict = None,
                         **kwargs):
    """
    Computing correlations between all node pairs

    Parameters
    ----------
    :param method: str, optional, default 'pearson'
        Method to use for correlation calculation. Available
        options are: pearson, kendall and spearman

    :param significance: float, optional, default 0.05
        Significance threshold for corrected pvalues

    :param overwrite: bool, optional, default False
        If True previously computed correlations are overwritten

    :param correct_args: dict, optional
        Arguments to pass to statsmodels.stats.multitest.multipletests
        for multiple test correction

    :param kwargs:
        keyword arguments to pass to the respective scipy.stats method

    """
    self._correlation_computation_(attr="correlations",
                                   method=method, significance=significance,
                                   overwrite=overwrite, correct_args=correct_args,
                                   **kwargs)


def compute_partial_correlations(self,
                                 estimator: str = "GraphLasso",
                                 significance: float = 0.05,
                                 overwrite: bool = False,
                                 correct_args: dict = None,
                                 **kwargs):
    """
    Computing correlations between all node pairs

    Parameters
    ----------
    :param estimator: str, optional, default 'GraphLasso'
        Method to use for partial correlation estimation. Available
        options are: GraphLasso, LedoitWolf and empirical

    :param significance: float, optional, default 0.05
        Significance threshold for corrected p-values. Only relevant
        if sample to feature ratio is large enough to compute
        Fisher's z-transform

    :param overwrite: bool, optional, default False
        If True previously computed correlations are overwritten

    :param correct_args: dict, optional
        Arguments to pass to statsmodels.stats.multitest.multipletests
        for multiple test correction

    :param kwargs:
        keyword arguments to pass to the respective scipy.stats method


    Raises
    ------
    ValueError
        If groups or data are not of the correct type


    Warns
    -----
    If 'data' or 'groups' are already set but provided again
    """
    self._correlation_computation_(attr="partial_correlations",
                                   estimator=estimator, significance=significance,
                                   overwrite=overwrite, correct_args=correct_args,
                                   **kwargs)


def compute_correlation_changes(self, partial_corrs: bool = False,
                                data: pd.DataFrame = None,
                                groups: pd.Series = None,
                                pval_change: bool = True,
                                overwrite: bool = True):
    """
    Computing changes of partial correlations between different conditions

    Parameters
    ----------
    :param partial_corrs: bool, optional, default False
        Whether to use partial correlations

    :param data: pd.DataFrame or str, optional
        Used to overwrite self.data if given. Required
        if no lipid data was added before. If str it
        assumed to be a csv file with samples in columns.

    :param groups: pd.Series or str, optional
        Used to overwrite self.groups if given. Required
        if no groups were added before. If str it
        assumed to be a csv or txt file.

    :param pval_change: bool, optional, default True
        Whether to compute categories or absolute values

    :param overwrite: bool, optional, default False
        If True previously computed correlations are overwritten
    """
    self._check_data_()
    if partial_corrs:
        attr = "partial_correlations"
        attr_change = "partial_correlation_changes"
    else:
        attr = "correlations"
        attr_change = "correlation_changes"
    if self.interaction_attributes[attr] is None:
        raise ValueError(
            f"{attr} have not been computed yet!"
        )
    if self.interaction_attributes.get(attr_change) is None:
        self.interaction_attributes[attr_change] = {}

    self._set_data_groups_(data=data, groups=groups)
    # compute how correlations/partial correlations change between groups
    # => should be mostly referring to from significant to unsignificant
    # or vice-versa
    # TODO: which metrics to use
    for comb in self.comparisons:
        if not overwrite:
            if self.interaction_attributes[attr_change].get(tuple(comb)) is not None:
                continue
            elif self.interaction_attributes[attr_change].get(tuple(comb[0], comb[1])) is not None:
                continue
        if pval_change:
            if (self.interaction_attributes[f"{attr}_pvals"][comb[0]] < 0).all() or \
                    (self.interaction_attributes[f"{attr}_pvals"][comb[1]] < 0).all():
                raise SignificanceTestError(
                    "Too few samples for the given number of features to compute a fisher's z-transform."
                )
            corr_changes = correlation_change(
                self.interaction_attributes[attr][comb[0]],
                self.interaction_attributes[attr][comb[1]]
            )
        else:
            corr_changes = self.interaction_attributes[attr][comb[0]] - \
                           self.interaction_attributes[attr][comb[1]]
        self.interaction_attributes[attr_change][tuple(comb)] = corr_changes


def compute_fold_changes(self, data_is_log: bool = True, log_func=np.log2):
    """
    Computing (log) fold-changes

    Parameters
    ----------
    :param data_is_log: bool, optional, default False
        Indicating whether data is log-transformed

    :param log_func: callable, optional, default np.log2
        Which log function to use, in case data_is_log is False
    """
    # TODO: documentation
    self._check_data_()
    if self.groups is None or self.data is None:
        raise ValueError("fold changes cannot be computed when no groups or data is given")
    if self.lipid_attributes.get("fold_changes") is None:
        self.lipid_attributes["fold_changes"] = {
            tuple(comparison): fold_changes(self.data, self.groups,
                                            comparison, data_is_log,
                                            log_func).fillna(0).to_dict()
            for comparison in self.comparisons
        }
    else:
        for comparison in self.comparisons:
            comp_st = tuple(comparison)
            if self.lipid_attributes["fold_changes"].get(comp_st) is None:
                fcs = fold_changes(self.data, self.groups,
                                   comparison, data_is_log,
                                   log_func).fillna(0).to_dict()
                self.lipid_attributes["fold_changes"][comp_st] = fcs


def compute_pvalues(
        self, round_vals: bool = False,
        method: str = "ttest"
):
    """
    Computing p-values

    Parameters
    ----------
    :param round_vals: bool, optional, default False
        If True pvalues will be rounded to four digits

    :param method: str, optional, default 'ttest'
        Which test to use. Available options are:
        'ttest', 'wilcoxon', '' and ''
    """
    self._check_data_()
    # computing p-values
    if self.lipid_attributes.get("pvalues") is None:
        pvals = {tuple(comparison): binary_test(self.data, self.groups,
                                                comparison, method=method)
                 for comparison in self.comparisons}
        nlog_pvals = {(comp[0], comp[1]): (-_pandas_log_(parr)).to_dict()
                      for comp, parr in pvals.items()}

        self.lipid_attributes["pvalues"] = {key: val.to_dict() for key, val in pvals.items()}
        self.lipid_attributes["nlog_pvalues"] = nlog_pvals
    else:
        for comparison in self.comparisons:
            comp_st = tuple(comparison)
            if self.lipid_attributes["pvalues"].get(comp_st) is None:
                pval = binary_test(self.data, self.groups,
                                   comparison)
                self.lipid_attributes["pvalues"][comp_st] = pval.to_dict()
                self.lipid_attributes["nlog_pvalues"][comp_st] = (-_pandas_log_(pval)).to_dict()
