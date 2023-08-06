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
from __future__ import annotations
from typing import Union, Callable, Tuple, Set, List, Dict

import networkx as nx
import numpy as np
import pandas as pd
from scipy import linalg, stats
from sklearn.covariance import (
    GraphicalLasso,
    LedoitWolf,
    empirical_covariance,
    ShrunkCovariance
)
from statsmodels.stats.moment_helpers import cov2corr
from statsmodels.stats.multitest import multipletests
from typing import Iterable, Optional
from .exceptions import CorrelationError, PartialCorrelationError
from .lipid import FA, Lipid
from .reaction import Reaction
import seaborn as sns
import matplotlib.pyplot as plt
import math
import pkg_resources
import json


lipid_colours = json.load(
    open(pkg_resources.resource_filename('linex2', 'templates/lipid_colours.json'), 'r')
)


def partial_correlations(data: pd.DataFrame,
                         estimator: str = "GraphLasso",
                         **kwargs) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Computing all feature partial correlations. Implementation based on
    Whittaker (1990) and the R package pppcor

    Parameters
    ----------
    :param data: pd.DataFrame, samples in rows
    :param estimator: str, 'empirical', 'GraphLasso', 'Shrinkage' or 'LedoitWolf', covariance estimator
    :return: tuple of pd.Series with partial correlations and pvalues, indices are data.columns
    """
    # computing covariance matrix
    if estimator == "empirical":
        try:
            cov = empirical_covariance(data, **kwargs)
        # TODO: what other errors can occur?
        except ValueError:
            raise PartialCorrelationError(
                f"Invalid values for empirical covariance calculation!",
                estimator
            )
    elif estimator == "GraphLasso":
        # TODO: should we use GraphicalLassoCV here?
        try:
            graph_lasso = GraphicalLasso()
            graph_lasso.fit(data)
            cov = graph_lasso.covariance_
        except ValueError:
            raise PartialCorrelationError(
                f"Invalid values for GraphLasso partial correlation calculations!",
                estimator
            )

    elif estimator == "LedoitWolf":
        try:
            lw = LedoitWolf()
            lw.fit(data)
            cov = lw.covariance_
        except ValueError:
            raise PartialCorrelationError(
                f"Invalid values for Ledoit-Wolf partial correlation calculations!",
                estimator
            )
    elif estimator == "GraphLasso":
        try:
            shrunk = ShrunkCovariance()
            shrunk.fit(data)
            cov = shrunk.covariance_
        except ValueError:
            raise PartialCorrelationError(
                f"Invalid values for GraphLasso partial correlation calculations!",
                estimator
            )
    else:
        raise ValueError(
            f"Estimator must be one of ['GraphLasso', 'Shrinkage', 'LedoitWolf', 'empirical'], not {estimator}"
        )
    # inverse covariance matrix
    try:
        inv_cov = linalg.inv(cov)
    except ValueError:
        raise PartialCorrelationError(
            f"Invalid values in covariance matrix inversion",
            estimator
        )
    # partial correlation matrix
    pcor = -cov2corr(inv_cov)
    np.fill_diagonal(pcor, 1)
    # p-values from fisher's z-transform
    n, m = data.shape
    fact = n - (m - 2) - 3
    pvals = -np.ones(pcor.shape)
    if fact > 0:
        stats_ = np.sqrt(fact) * .5 * np.log((1 + pcor)/(1 - pcor))
        # TODO: double check if normality actually is true
        pvals = 2 * stats.norm.cdf(1 - stats_)
    else:
        print("p-values could not be calculated due to too few samples")

    pcor_df = pd.DataFrame(pcor, index=data.columns,
                           columns=data.columns)
    return pcor_df, pvals


def correlations(data: pd.DataFrame,
                 method: str = "spearman",
                 **kwargs) -> Tuple[pd.DataFrame, np.ndarray]:
    methods = {
        "pearson": stats.pearsonr,
        "spearman": stats.spearmanr,
        "kendall": stats.kendalltau
    }

    if method not in methods.keys():
        raise ValueError(
            f"'method' must be one of {list(methods.keys())}"
        )

    if data.shape[1] < 2:
        cors = pd.DataFrame(columns=data.index,
                            index=data.index)
        pvals = pd.DataFrame(columns=data.index,
                             index=data.index)
        return cors, pvals.values

    cors = np.zeros(2*[data.shape[0]])
    pvals = np.zeros(2*[data.shape[0]])
    for i in range(data.shape[0] - 1):
        for j in range(i + 1, data.shape[0]):
            try:
                cor_, pval_ = methods[method](data.values[i, :],
                                              data.values[j, :],
                                              **kwargs)
            except ValueError:
                if data.iloc[i, :].isna().values.any() or data.iloc[j, :].isna().values.any():
                    cor_ = np.nan
                    pval_ = np.nan
                else:
                    lipids = (data.index[i], data.index[j])
                    raise CorrelationError(
                        f"Invalid values at lipids {lipids} during correlation calculations.\n",
                        lipids
                    )
            cors[i, j] = cor_
            cors[j, i] = cor_
            pvals[i, j] = pval_
            pvals[j, i] = pval_

    cor_df = pd.DataFrame(cors, columns=data.index,
                          index=data.index)
    return cor_df, pvals


def _matrix_pval_correction_(data: Union[pd.DataFrame, np.ndarray],
                             **kwargs) -> np.ndarray:
    """
    Multiple test correction on a symmetric(!) p-value matrix

    Parameters
    ----------
    data
    kwargs

    Returns
    -------

    """
    lidx = np.tril_indices_from(data, -1)

    if isinstance(data, pd.DataFrame):
        pval_corr = multipletests(data.values[lidx], **kwargs)
    else:
        pval_corr = multipletests(data[lidx], **kwargs)

    corrected = np.zeros(data.shape)
    # corrected[uidx] = pval_corr[1]
    corrected[lidx] = pval_corr[1]
    corrected += corrected.T

    return corrected


def generalised_log(data, c=1e-5,
                    log_fun=np.log2):
    return log_fun(data + np.sqrt(data ** 2 + c))


def fold_changes(data: pd.DataFrame,
                 groups: Union[np.ndarray, pd.Series],
                 compare_groups: Union[Tuple[str], List[str]],
                 data_is_log: bool = True,
                 log_func=generalised_log,
                 to_log: bool = False) -> pd.Series:
    """
    Helper function for computing (log-) fold changes of means of samples groups.

    Parameters
    ----------
    data : data from which to compute fold changes. Samples must be in columns
    groups : array of sample groups in the order of data.columns
    compare_groups : list of strings of the two groups to compare
    data_is_log : boolean, indicating whether input data is already log-transformed
                  if False, data will be in-line log-transformed
    log_func : function for log transformation
    to_log: boolean, whether to do log transformation if data_is_log is False

    Returns
    -------
    pd.Series of size data.shape[0] containing fold changes
    """
    group1 = data.loc[:, groups == compare_groups[0]]
    group2 = data.loc[:, groups == compare_groups[1]]
    if data_is_log:
        fcs = np.nanmean(group1, axis=1) - np.nanmean(group2, axis=1)
        return pd.Series(fcs, index=data.index)
    elif to_log:
        fcs = np.nanmean(log_func(group1 + 1), axis=1) - np.nanmean(log_func(group2 + 1), axis=1)
        return pd.Series(fcs, index=data.index)
    else:
        m1 = np.nanmean(group1, axis=1)
        m2 = np.nanmean(group2, axis=1)
        fcs = pd.Series(np.zeros(data.shape[0]),
                        index=data.index)
        for i in range(data.shape[0]):
            if m1[i] >= m2[i]:
                if m2[i] == 0:
                    fcs[i] = np.nan
                else:
                    fcs[i] = m1[i]/m2[i]
            else:
                if m1[i] == 0:
                    fcs[i] = np.nan
                else:
                    fcs[i] = -(m2[i] / m1[i])
        return fcs


def binary_test(data: pd.DataFrame,
                groups: Union[np.ndarray, pd.Series],
                compare_groups: Union[List[str], Set[str], Tuple[str, str]],
                method: Union[str, Callable] = "ttest",
                p_adjust_method: str = "fdr_bh",
                **kwargs) -> pd.Series:
    methods = {
        "wilcoxon": stats.wilcoxon,
        "ttest": stats.ttest_ind
    }
    if isinstance(method, str):
        test = methods[method]
    else:
        test = method
    # subsetting groups
    if np.unique(groups).size == 2:
        f_groups = groups
    else:
        f_groups = groups[np.isin(groups, compare_groups)]
    # subsetting data to only contain groups of interest
    sub_data = data.loc[:, f_groups.index]
    # computing feature-wise p-values
    pvals = sub_data.apply(lambda x: test(x.values[f_groups == compare_groups[0]],
                                          x.values[f_groups == compare_groups[1]],
                                          **kwargs)[1],
                           axis=1)
    # NOTE: nans cause multipletest to return nans only!
    pvals[pvals.isna()] = 1
    return pd.Series(multipletests(pvals.values, method=p_adjust_method)[1],
                     index=pvals.index)


def unique_elements(data: Union[pd.DataFrame, pd.Series, dict, SymmetricMatrix]) -> np.ndarray:
    """
    Helper to extract all unique elements from a data frame or a series.<br>

    For a pd.Series the result is equivalent to pd.Series.unique().values

    Parameters
    ----------
    data : a general value

    Returns
    -------

    """
    if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        nas = data.isna()
        na_free = data.values[np.invert(nas)]
    elif isinstance(data, SymmetricMatrix):
        try:
            na_free = data.data[~np.isnan(data.data)]
        # catching numpy being unable to use isnan with string objects
        except TypeError:
            na_free = data.data[~pd.DataFrame(data.data).isna().values]
    else:
        vals = np.array(list(data.values()))
        try:
            na_free = vals[~np.isnan(vals)]
        # catching numpy being unable to use isnan with string objects
        except TypeError:
            na_free = vals[[val != np.nan for val in vals]]
    return np.unique(na_free)


def correlation_change(c_s_: SymmetricMatrix,
                       c_t_: SymmetricMatrix) -> SymmetricMatrix:

    if not c_s_.shape == c_t_.shape:
        raise ValueError(
            "Both input matrices need to have the same input dimensions!"
        )
    c_s_.fillna(0)
    c_t_.fillna(0)
    # make sure c_s_ and c_t_'s indices are ordered the same
    c_t_.align(c_s_)
    x_ = np.tril_indices_from(c_s_.data)
    x = c_s_.data[x_]
    y = c_t_.data[x_]

    inter = np.array(x.size * [""], dtype=object)
    # unsignificant
    inter[(x == 0) & (y == 0)] = "unsignificant"
    # significant vs. unsignificant
    inter[((x != 0) & (y == 0))] = "significant to unsignificant"
    inter[((x == 0) & (y != 0))] = "unsignificant to significant"
    # unchanged significant
    # NOTE: needs to come before the next two or else will overwrite
    inter[(x != 0) & (y != 0)] = "unchanged significant"
    # both significant
    inter[(x > 0) & (y < 0)] = "positive to negative"
    inter[(x < 0) & (y > 0)] = "negative to positive"

    ret = np.array(c_s_.shape[1]*[c_s_.shape[0]*[""]],
                   dtype=object)
    ret[x_] = inter
    ret.T[x_] = inter
    return SymmetricMatrix(
        pd.DataFrame(ret, columns=c_s_.index,
                     index=c_s_.index)
    )


def adapt_data(dat: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    indices = dat.index.values
    fi = []
    newname = []
    for i in range(len(indices)):
        if indices[i] in mapping.keys():
            fi.append(i)
            newname.append(mapping[indices[i]])
    d = dat.copy()
    d = d.iloc[fi, :]
    d.index = pd.Series(newname)

    return d


class SymmetricMatrix:
    __slots__ = [
        "data", "idx_map"
    ]

    data: np.ndarray
    idx_map: Dict[str, int]

    def __init__(self, data: pd.DataFrame = None):
        # TODO: use only an upper triangular matrix (how in python?)
        if data is not None:
            self.set_data(data)

    def set_data(self, data: pd.DataFrame):
        if any(data.index != data.columns):
            raise ValueError(
                "Input data must be a symmetric matrix"
            )
        self.data = data.values
        self.idx_map = {name: idx for idx, name in enumerate(data.index.values)}

    def _get_idxs_(self, it):
        if isinstance(it, slice):
            if not (it.start is None and it.stop is None and it.step is None):
                raise ValueError("Slicing between index ranges not supported")
            return it
        elif isinstance(it, str):
            return self.idx_map[it]
        elif isinstance(it, Iterable):
            return [self.idx_map[xi] for xi in it]

    def __lt__(self, other):
        return self.data.__lt__(other)

    def __gt__(self, other):
        return self.data.__gt__(other)

    def __eq__(self, other):
        if other is None:
            return self.is_empty()
        elif isinstance(other, SymmetricMatrix):
            return self.data == other.data
        elif isinstance(other, np.ndarray):
            return self.data == other
        else:
            raise ValueError(
                f'No comparison implemented for type {type(other).__name__}.'
            )

    def __ne__(self, other):
        return self.data.__ne__(other)

    def __neg__(self, other):
        return self.data.__neg__(other)

    def __add__(self, other):
        return self.data.__add__(other)

    def __sub__(self, other):
        return self.data.__sub__(other)

    def __getitem__(self, item):
        if isinstance(item, list) or isinstance(item, tuple) or isinstance(item, np.ndarray):
            if len(item) != 2:
                raise ValueError("Only two dimensional slicing supported!")
            return self.data[self._get_idxs_(item[0]), self._get_idxs_(item[1])]
        elif isinstance(item, str):
            return self.data[self.idx_map[item], self.idx_map[item]]
        else:
            raise ValueError(f"{type(item).__name__} not a supported type for slicing")

    def get(self, row_key, col_key, default=None):
        row_idx = self.idx_map.get(row_key)
        col_idx = self.idx_map.get(col_key)
        if row_idx is None or col_idx is None:
            return default
        # since data is a symmetric matrix, the above check
        # is sufficient to guarantee this slice works
        return self.data[row_idx, col_idx]

    @property
    def keys(self):
        return self.idx_map.keys()

    def __repr__(self):
        if hasattr(self, "data"):
            return self.data.__repr__()
        return "[]"

    # to have a dict-like behaviour for if SymmetricMatrix: do...
    def __nonzero__(self):
        return self.is_empty()

    def is_empty(self):
        return not hasattr(self, "data")

    @property
    def shape(self):
        return self.data.shape

    @property
    def index(self):
        idx = np.empty(len(self.idx_map), dtype=object)
        for key, val in self.idx_map.items():
            idx[val] = key
        return idx

    def fillna(self, value, inplace: bool = True) -> Union[None, np.ndarray]:
        nans = np.isnan(self.data)
        if inplace:
            self.data[nans] = value
        else:
            data = self.data.copy()
            data[nans] = value
            return data

    def align(self, matrix: SymmetricMatrix):
        if len(self.idx_map) != len(matrix.idx_map):
            raise ValueError(
                f"'matrix' must not have a different number of entries"
            )
        key_sort = np.empty(len(self.idx_map), dtype=np.int32)
        idx_map_upd = {}
        # TODO: make sure this working as expected (i.e. double check!)
        try:
            for key, val in matrix.idx_map.items():
                key_sort[self.idx_map[key]] = val
                idx_map_upd[key] = val
        except KeyError:
            unmatched = [key for key in matrix.idx_map.keys()
                         if self.idx_map.get(key) is None]
            raise KeyError(
                f"The following keys could not be found: {unmatched}"
            )
        self.data = self.data[key_sort, :][:, key_sort]
        self.idx_map = idx_map_upd

    def to_csv(self, *args, **kwargs):
        indices = np.empty(len(self.idx_map), dtype='<U1')
        for key, idx in self.idx_map.items():
            indices[idx] = key
        pd.DataFrame(
            self.data, columns=indices, index=indices
        ).to_csv(*args, **kwargs)


def extend_class_fa(class_fa: Dict[str, List[FA]],
                    lipid_dict: Dict[str, List[Lipid]],
                    add_to_all: bool = True) -> Dict[str, List[FA]]:
    """
    Extend class specific fatty acids with known fatty acids from molecular species for that class

    Parameters
    ----------
    :param class_fa: Dict[str, List[FA]]
        Class fatty acids as generated by the function "parse_fatty_acids".

    :param lipid_dict: Dict[str, List[Lipid]]
        Dict of Lipids. With Lipid class as key and list of Lipids as values.

    :param add_to_all: bool, default=True
        Add fatty acids of lipid classes, which are not specified to fatty acids of all unspecified classes.

    Returns
    -------
    :return:
        Extended dict of class specific fatty acids
    """

    # Make copy of class_fa dict
    new_class_fa = {x: class_fa[x].copy() for x in class_fa.keys()}

    # Loop over all classes
    for cls in lipid_dict.keys():

        if cls in new_class_fa.keys():
            add_to = cls
        else:
            if add_to_all:
                add_to = "all"
            else:
                continue

        class_lipids = lipid_dict[cls]
        # Loop over every lipid
        for lip in class_lipids:
            # Do not use fatty acids, if molecular species is inferred from sum species
            if not lip.converted_to_mol_spec():
                if lip.is_molecular_species():
                    for fa in lip.get_fas():
                        if fa not in new_class_fa[add_to]:
                            new_class_fa[add_to].append(fa)

    return new_class_fa


def check_databases(dbs: Union[List[str], Tuple[str]]) -> bool:
    counter = 0
    if "Reactome" in dbs:
        counter += 1
    if "Rhea" in dbs:
        counter += 1

    if (len(dbs) > counter) or (counter < 1):
        raise ValueError("Selected databases must be 'Reactome', 'Rhea' or ('Reactome', 'Rhea').")
    else:
        return True


def combine_reactions(reactions1: List[Reaction], reactions2: List[Reaction]) -> List[Reaction]:

    # copy content from reaction1
    reactions = [reac for reac in reactions1]

    # loop over all other reactions
    for r2 in reactions2:
        found = False
        for r1i in range(len(reactions)):
            if r2.participation_equality(reactions[r1i]):
                reactions[r1i].extend_enzyme_ids(r2.get_enzyme_id())
                reactions[r1i].extend_uniprot(r2.get_uniprot())
                reactions[r1i].extend_gene_name(r2.get_gene_name())
                reactions[r1i].extend_nl_participants(r2.get_nl_participants())
                found = True
                break
        if not found:
            reactions.append(r2)

    return reactions


def plot_boxplot(data: Dict[str, pd.DataFrame],
                 plot_n_col: int = 3,
                 plot_fig_size: Tuple[int, int] = (10, 18),
                 plot_hspace: float = 0.4,
                 difference_dist: bool = False,
                 as_subplots: bool = True,
                 z_scores: bool = True
                 ) -> plt.Figure:
    if as_subplots:
        def plot_boxes(ax, data, key, difference_dist, z_scores):
            if z_scores:
                data["value"] = (data['value'] - data['value'].mean()) / data['value'].std()
            if "groups" in data.columns:
                sns.boxplot(
                    ax=ax,
                    data=data,
                    x="groups",
                    y="value",
                ).set_title(key)
            else:
                sns.boxplot(
                    ax=ax,
                    data=data,
                    y="value",
                ).set_title(key)
            if difference_dist:
                ax.set(ylabel='Ratio difference')
            else:
                ax.set(ylabel='Ratio')
        return plot_template(
            data, plot_boxes, plot_n_col, plot_fig_size,
            plot_hspace, difference_dist=difference_dist,
            z_scores=z_scores
        )
    else:
        fig, ax = plt.subplots(figsize=plot_fig_size)
        dfs = []
        for reaction, df in data.items():
            if z_scores:
                df["value"] = (df['value'] - df['value'].mean()) / df['value'].std()
            df['Reaction'] = reaction
            dfs.append(df)
        df_data = pd.concat(dfs)

        if 'groups' in df_data.columns:
            sns.boxplot(
                ax=ax,
                data=df_data,
                y="value",
                x='Reaction',
                hue='groups'
            )
        else:
            sns.boxplot(
                ax=ax,
                data=df_data,
                y="value",
                x='Reaction'
            )
        if difference_dist:
            ax.set(ylabel='Ratio difference')
        else:
            ax.set(ylabel='Ratio')
        return fig


def plot_histogram(data: Dict[str, pd.DataFrame],
                   plot_n_col: int = 3,
                   plot_fig_size: Tuple[int, int] = (10, 18),
                   plot_hspace: float = 0.4,
                   difference_dist: bool = False
                   ) -> plt.Figure:

    # Seaborn histplot tutorial: https://seaborn.pydata.org/generated/seaborn.histplot.html
    # plotting tutorial: https://realpython.com/python-matplotlib-guide/
    def plot_hist(ax, data, key, difference_dist):
        if "groups" in data.columns:
            sns.histplot(ax=ax,
                         data=data,
                         x="value",
                         hue="groups",
                         element="poly",
                         stat="count"
                         ).set_title(key)
        else:
            sns.histplot(ax=ax,
                         data=data,
                         x="value",
                         element="poly",
                         stat="count"
                         ).set_title(key)
        if difference_dist:
            ax.set(xlabel='Ratio difference', ylabel='Count')
        else:
            ax.set(xlabel='Ratio', ylabel='Count')

    return plot_template(
        data, plot_hist, plot_n_col, plot_fig_size,
        plot_hspace, difference_dist=difference_dist
    )


def get_class_reaction(raw_id: str, cls_reacs: List[Reaction]) -> Union[None, Reaction]:
    if "\nFA: " in raw_id:
        tmp_id = raw_id.split("\nFA: ")[0]
    else:
        tmp_id = raw_id
    for i in cls_reacs:
        if i.get_enzyme_id() == tmp_id:
            return i


def reaction_titles(raw_id: str, cls_reacs: Optional[List[Reaction]] = None,
                    class_reaction: Optional[Reaction] = None,
                    pairs=None) -> Union[None, str]:
    fa_spec = False
    if "\nFA: " in raw_id:
        fa_spec = True
    if class_reaction is None:
        if cls_reacs is None:
            raise ValueError("Either 'class_reacs' or 'class_reaction' have to be specified!")
        class_reaction = get_class_reaction(raw_id, cls_reacs)
        if class_reaction is None:
            return None
    reaction_str = class_reaction.short_str(nice=True)
    if fa_spec:
        reaction_str += "\nFA: " + raw_id.split("\nFA: ")[1]
    if reaction_str == "":
        reaction_str = raw_id
    if pairs:
        reaction_str += "\nPair: " + pairs
    return reaction_str


def compute_ratios(unique_enzyme_list: List[str],
                   enzyme_structure_dict: Dict[str, str],
                   gr: nx.Graph,
                   reverse_mapping: Dict[str, str],
                   user_data: pd.DataFrame,
                   class_reactions: List[Reaction],
                   edge_attr: str,
                   difference_as_change: bool
                   ) -> Dict[str, pd.DataFrame]:
    reaction_ids: Dict[str, List[List[Union[str, Dict]]]] = {}
    multi_reaction_enzymes: Dict[str, List[str]] = {}
    for ed in gr.edges:
        tmp_edge_data = gr.get_edge_data(*ed)
        if tmp_edge_data[edge_attr] in unique_enzyme_list:
            if tmp_edge_data["reaction_id"] in reaction_ids.keys():
                reaction_ids[tmp_edge_data["reaction_id"]].append([ed[0], ed[1], tmp_edge_data])
            else:
                reaction_ids[tmp_edge_data["reaction_id"]] = [[ed[0], ed[1], tmp_edge_data]]
            if tmp_edge_data['reaction_structure'] != '1,1':
                # storing reaction id of multi-edge reactions
                multi_reaction_enzymes.setdefault(tmp_edge_data[edge_attr], []).append(tmp_edge_data['reaction_id'])

    df_list = {}
    for reac in unique_enzyme_list:
        counter = 0
        ratio_df = pd.DataFrame({})
        enzyme_struct = enzyme_structure_dict[reac].split(';')
        # length of 1 would be fatty acid modification => penalty
        # 1 substrate 1 product reaction
        if enzyme_struct[0] == '1,1':
            for edge in gr.edges:
                if gr.edges[edge][edge_attr] == reac and gr.edges[edge]['reaction_type'] != 'L_FAmodify':
                    tmp_edge = [reverse_mapping[edge[0]], reverse_mapping[edge[1]]]
                    if difference_as_change:
                        tmp_ratio = user_data[tmp_edge[0]] - user_data[tmp_edge[1]]
                    else:
                        tmp_ratio = user_data[tmp_edge[0]] / user_data[tmp_edge[1]]
                    if counter == 0:
                        ratio_df = pd.DataFrame({f'{tmp_edge[0]} - {tmp_edge[1]}': tmp_ratio})
                        counter += 1
                    else:
                        ratio_df = ratio_df.assign(**{f'{tmp_edge[0]} - {tmp_edge[1]}': tmp_ratio})
                        counter += 1
            df_list[reaction_titles(reac, class_reactions)] = ratio_df.copy()
        # multi substrate/product reaction
        else:
            for reaction in multi_reaction_enzymes[reac]:
                edge_list = reaction_ids[reaction]
                substrates = []
                products = []
                for edge in edge_list:
                    if edge[2]['l1_type'] == 'substrate':
                        substrates.append(user_data[reverse_mapping[edge[0]]])
                        products.append(user_data[reverse_mapping[edge[1]]])
                    else:
                        substrates.append(user_data[reverse_mapping[edge[1]]])
                        products.append(user_data[reverse_mapping[edge[0]]])
                if difference_as_change:
                    tmp_ratio = sum(products) - sum(substrates)
                else:
                    tmp_ratio = math.prod(products) / math.prod(substrates)
                if counter == 0:
                    ratio_df = pd.DataFrame({reaction: tmp_ratio})
                    counter += 1
                else:
                    ratio_df = ratio_df.assign(**{reaction: tmp_ratio})
                    counter += 1
            df_list[reaction_titles(reac, class_reactions)] = ratio_df.copy()
    return df_list


def plot_lineplot(data: Dict[str, pd.DataFrame],
                  plot_n_col: int = 3,
                  plot_fig_size: Tuple[int, int] = (10, 18),
                  plot_hspace: float = 0.4,) -> plt.Figure:
    def plot_line(ax, data, key):
        sns.lineplot(ax=ax,
                     data=data,
                     x="variable",
                     y="FC",
                     marker="o",
                     hue="groups"
                     ).set_title(key)

        ax.set(xlabel='Total chain length', ylabel='Abundance')

    return plot_template(
        data, plot_line, plot_n_col, plot_fig_size,
        plot_hspace
    )


def plot_networks(networks: Dict[str, nx.Graph],
                  scores: Dict[str, float],
                  p_values: Dict[str, float],
                  plot_n_col: int = 3,
                  plot_fig_size: Tuple[int, int] = (10, 18),
                  plot_hspace: float = 0.4) -> Tuple[Dict[str, nx.Graph], plt.Figure]:
    def plot_net(ax, data, key, scores, p_values):
        pos = nx.spring_layout(data)
        # labels = nx.get_edge_attributes(network, 'objective')
        # for key in labels:
        #     labels[key] = np.round(labels[key], 2)
        # nx.draw_networkx(data, pos, font_size=8, ax=ax)
        # nx.draw_networkx_edge_labels(network, pos, edge_labels=labels)
        lipid_nodes = [node for node in data.nodes
                       if data.nodes[node]['node_molecule_type'] == 'Lipid']
        nx.draw_networkx_nodes(
            data,
            pos,
            nodelist=lipid_nodes,
            node_shape='o',
            node_color=[lipid_colours[data.nodes[node]['lipid_class']]
                        for node in lipid_nodes],
            ax=ax
        )
        nx.draw_networkx_nodes(
            data,
            pos,
            nodelist=[node for node in data.nodes
                      if data.nodes[node]['node_molecule_type'] != 'Lipid'],
            node_shape='^',
            node_color='grey',
            ax=ax
        )
        nx.draw_networkx_edges(
            data, pos,
            edge_color='lightgrey',
            style=['solid' if not data.edges[edge].get('enzyme_edge', False) else 'dashed' for edge in data.edges],
            ax=ax
        )
        nx.draw_networkx_labels(
            data,
            pos,
            labels={
                node: data.nodes[node]['data_name'] if data.nodes[node]['node_molecule_type'] == 'Lipid'
                else data.nodes[node]['representation_id']
                for node in data.nodes
            },
            font_size=7, ax=ax
        )
        ax.set_title(key + f', score: {np.round(np.max(scores[key]), 3)}, p-value: {p_values[key]}')
        ax.axis('off')

    for name, net in networks.items():
        colours = {node: lipid_colours.get(net.nodes[node].get('lipid_class'), 'grey')
                   for node in net.nodes}
        shapes = {node: 'dot' if net.nodes[node]['node_molecule_type'] == 'lipid_class' else '^'
                  for node in net.nodes}
        labels = {node: node for node in net.nodes}
        nx.set_node_attributes(net, colours, "color")
        nx.set_node_attributes(net, shapes, "shape")
        nx.set_node_attributes(net, labels, "label")
        networks[name] = net

    return networks, plot_template(networks,
                                   plot_net,
                                   plot_n_col,
                                   plot_fig_size,
                                   plot_hspace,
                                   scores=scores,
                                   p_values=p_values)


def plot_template(data: Dict[str, any],
                  plot_function,
                  plot_n_col: int = 3,
                  plot_fig_size: Tuple[int, int] = (10, 18),
                  plot_hspace: float = 0.4,
                  **kwargs) -> plt.Figure:
    if len(data) == 1:
        fig, ax = plt.subplots(figsize=plot_fig_size)
        for key, ratio_df in data.items():
            plot_function(
                ax=ax,
                data=ratio_df,
                key=key,
                **kwargs
            )
        return fig

    columns = plot_n_col
    rows = math.ceil(len(data) / columns)
    single_row = rows < 2 or columns < 2
    rows = rows if rows > 0 else 1
    columns = columns if columns > 0 else 1
    fig, ax = plt.subplots(nrows=rows,
                           ncols=columns, figsize=plot_fig_size)
    fig.subplots_adjust(wspace=0.2,
                        hspace=plot_hspace)

    # loop over all dfs
    counter = 0
    for key, ratio_df in data.items():
        if single_row:
            plot_function(
                ax=ax[counter],
                data=ratio_df,
                key=key,
                **kwargs
            )
        else:
            plot_function(
                ax=ax[counter // columns, counter % columns],
                data=ratio_df,
                key=key,
                **kwargs
            )
        # At the end of the loop
        counter += 1
    # Delete last Axes if odd number of DataFrames
    while counter < ax.size:
        if single_row:
            fig.delaxes(ax[counter])
        else:
            fig.delaxes(ax[counter // columns, counter % columns])
        counter += 1

    return fig


def _add_missing_rows_(
    data: pd.DataFrame, species: List[str]
) -> pd.DataFrame:
    # test if this is really efficient or if we should
    # another way of adding rows
    dummy = pd.Series(index=data.columns)
    full_data = data.T.to_dict()
    for spec in species:
        if full_data.get(spec) is None:
            full_data[spec] = dummy
    return pd.DataFrame(full_data).T

