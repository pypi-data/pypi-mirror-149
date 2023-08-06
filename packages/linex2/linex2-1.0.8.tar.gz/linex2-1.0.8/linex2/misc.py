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
from typing import Union, List, Callable, Tuple, Dict, Any
import pandas as pd
import numpy as np
from matplotlib.pyplot import Line2D


def _size_legend_(extrema: tuple, scale: tuple = None,
                  nodes: bool = True, **kwargs) -> List[Line2D]:
    def size_from_scale(step: int, scale: tuple, extrema: tuple):
        inter = (step - scale[0]) / (scale[1] - scale[0])
        return inter * (extrema[1] - extrema[0])

    if scale is None:
        scale_steps = [abs(extrema[1] - extrema[0]) / 3 * i
                       for i in range(1, 5)]
        sizes = scale_steps
    else:
        scale_steps = [abs(scale[1] - scale[0]) / 3 * i
                       for i in range(1, 5)]
        sizes = [size_from_scale(step, scale, extrema)
                 for step in scale_steps]
    if nodes:
        handles = [Line2D([0], [0],
                          markersize=int(ms),
                          marker="o",
                          markerfacecolor="r",
                          label=round(lab, ndigits=4),
                          **kwargs)
                   for ms, lab in zip(scale_steps, sizes)]
    else:
        handles = [Line2D([0], [0], lw=int(lw),
                          color="r",
                          label=round(lab, ndigits=4),
                          **kwargs)
                   for lw, lab in zip(scale_steps, sizes)]
    return handles


def _range_scale_(
        x: Union[np.ndarray, pd.Series],
        a: Union[int, float], b: Union[int, float],
) -> Union[np.ndarray, pd.Series]:
    min_ = x.min()
    max_ = x.max()
    return ((x - min_) / (max_ - min_) * (b - a)) + a


def _pandas_log_(data: Union[pd.DataFrame, pd.Series],
                 log_fun: Callable = np.log10) -> Union[pd.DataFrame, pd.Series]:
    logged = data.copy()
    log_vals = log_fun(logged.values)
    if isinstance(data, pd.DataFrame):
        return pd.DataFrame(log_vals, index=data.index,
                            columns=data.columns)
    elif isinstance(data, pd.Series):
        return pd.Series(log_vals, index=data.index,
                         name=data.name)
    else:
        raise ValueError(
            "_pandas_log_ is only implemented for pd.Series and pd.DataFrame "
            f"not {type(data).__name__}"
        )


def _reaction_enzyme_annotation(src: str, tgt: str, enzyme: str) -> str:
    return f"{src} -> {tgt}: {enzyme}"


def _aggregate_species_(
        data: Union[pd.DataFrame, pd.Series] = None,
        species_axis: str = "columns"
) -> Union[pd.DataFrame, pd.Series]:
    if isinstance(data, pd.DataFrame):
        species = getattr(data, species_axis)
        dupl_mask = species.duplicated()
        duplicates = species[dupl_mask]
        if species_axis == "columns":
            agg_data = data.copy(deep=True).loc[:, ~dupl_mask]
            for dup_idx in duplicates:
                agg_data.loc[:, dup_idx] = data.loc[:, dup_idx].sum(axis=1)
        elif species_axis == "index":
            agg_data = data.copy(deep=True).loc[~dupl_mask, :]
            for dup_idx in duplicates:
                agg_data.loc[dup_idx, :] = data.loc[dup_idx, :].sum(axis=1)
        else:
            raise ValueError(
                "species_axis must be 'columns' or 'index' "
                f"not {species_axis}"
            )
        return agg_data
    elif isinstance(data, pd.Series):
        return data[~data.duplicated()]
    else:
        raise ValueError(
            "Data must be a pandas DataFrame or Series "
            f"not a {type(data).__name__}"
        )


def _tuple_to_string_(tup: Tuple[str, str]) -> str:
    return f"{tup[0]}_{tup[1]}"


def _get_sizes_report_nas_(
    attr: Dict[str, Any], keys, as_abs=False,
    default=None
):
    sizes = {}
    na_keys = []
    for node in keys:
        val = attr.get(node, default)
        if as_abs:
            val = abs(val)
        sizes[node] = val
        if np.isnan(val):
            na_keys.append(node)
    return sizes, na_keys
