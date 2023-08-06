import itertools

import numpy as np
import pandas as pd
from typing import Union, Tuple, Dict, List, Optional, Any
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import seaborn as sns
from .lipid import Lipid

N_COLS = 3
FUNCTION_NAMES = {
    Lipid.get_lipid_class: 'LipidClass',
    Lipid.sum_length: 'SumLength',
    Lipid.sum_dbs: 'SumDBs',
    Lipid.sum_ohs: 'SumOHs',
    Lipid.get_backbone: 'Backbone',
    Lipid.get_headgroup: 'Headgroup',
    Lipid.get_category: 'Category',
    Lipid.get_fa_long_chain_base: 'LongChainBase',
    Lipid.get_fa_lengths: 'FALength',
    Lipid.get_fa_dbs: 'FADBs'
}
DEFAULT_COLOUR = to_hex(plt.get_cmap('tab10')(0))


def _get_colours_(n: int) -> List[str]:
    if n < 11:
        colours = plt.get_cmap('tab10').colors
    elif n < 21:
        colours = plt.get_cmap('tab20').colors
    else:
        colours = plt.cm.rainbow(np.linspace(0, 1, n))
    return [to_hex(col) for col in colours]


def _ceiling_division_(a, b):
    return -(a // -b)


def _add_feature_combinations_(feature_matrix, lipid, features, n_combinations):
    for x in itertools.combinations(features, n_combinations):
        combined_feature = ' -- '.join(sorted(x))
        if combined_feature not in feature_matrix.index.values:
            feature_matrix = feature_matrix.append(pd.Series([0] * feature_matrix.shape[1],
                                                             index=feature_matrix.columns,
                                                             name=combined_feature))
        feature_matrix.loc[combined_feature, lipid.get_dataname()] += (1 / lipid.get_div_factor())
    return feature_matrix


def analysis_lipid_substructure(
    self, functions: list, feature_combinations: int = 1,
    combined: bool = False, single_n_combination: bool = False
) -> pd.DataFrame:
    """
    TODO: Tim

    Parameters
    ----------
    :param functions
    :param feature_combinations
    :param combined: bool, default=False
        Combine newly generated lipid substructures with the original lipid data and
        output the combined data frame.
    :param single_n_combination

    Returns
    -------
    :return: pd.DataFrame
        Data frame with lipid substructures as amounts for each sample.
        Optionally, the data frame is combined with the original lipid data.
    """
    # Set lipid weights
    lipid_dict = self._get_weighted_lipid_dict()

    # Construction of the feature weight matrix
    # This will later be multiplied with data matrix
    feature_matrix = self.data.T.drop(self.data.T.index.values)

    for cls in lipid_dict.keys():
        for lip in lipid_dict[cls]:
            # make list of all considered features
            tmp_features = list()
            # *category
            for ele in functions:
                if ele == Lipid.get_fas:
                    # **single
                    for i in ele(lip):
                        tmp_features.append(f"FA: {str(i)}")
                    # **combined
                    if len(ele(lip)) >= 2:
                        for x in itertools.combinations(ele(lip), 2):
                            tmp_features.append(f"FA: {str(sorted(x))}")
                    if len(ele(lip)) >= 3:
                        for x in itertools.combinations(ele(lip), 3):
                            tmp_features.append(f"FA: {str(sorted(x))}")
                    if len(ele(lip)) >= 4:
                        print("Combinations of 4 FA's are not implemented")
                else:
                    tmp_features.append(
                        f"{FUNCTION_NAMES.get(ele, str(ele).split(' ')[1].split('.')[1])} = {str(ele(lip))}"
                    )
            if single_n_combination:
                feature_matrix = _add_feature_combinations_(
                    feature_matrix, lip, tmp_features,
                    feature_combinations
                )
            else:
                count = 1
                while count <= feature_combinations:
                    feature_matrix = _add_feature_combinations_(
                        feature_matrix, lip, tmp_features,
                        count
                    )
                    count += 1
    if combined:
        return feature_matrix.dot(self.data).append(self.data)
    else:
        return feature_matrix.dot(self.data)


def _flatten_(data: pd.DataFrame):
    flat_x = []
    flat_y = []
    for column, column_data in data.items():
        nan_free_column = column_data.dropna()
        if not np.all(nan_free_column == 0):
            flat_x += nan_free_column.size * [column]
            flat_y += list(nan_free_column)
    return flat_x, flat_y


def _subplot_layout_(plots, **kwargs) -> Dict[str, Any]:
    n_rows = _ceiling_division_(len(plots), N_COLS)
    return {
        'grid': {'rows': n_rows, 'columns': N_COLS, 'pattern': 'independent'},
        'annotations': [
            {
                'text': lclass,
                'showarrow': False,
                'x': 0,
                'xref': f'x{i + 1} domain',
                'y': 1.15,
                'yref': f'y{i + 1} domain',
                **kwargs
            }
            for i, lclass in enumerate(sorted(plots.keys()))
        ]
    }


def _df_to_plotly_dict_(
    data: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
    plot_type: str = 'box', x_to_string: bool = True,
    y_to_string: bool = False
):
    if isinstance(data, pd.DataFrame):
        if 'Group' in data.keys():
            groups = data['Group']
            unique_groups = groups.unique()
            tmp_data = data.drop(columns='Group')
            colours = _get_colours_(unique_groups.size)
            plot_list = []
            for i, group in enumerate(sorted(unique_groups)):
                x, y = _flatten_(tmp_data.loc[groups == group, :])
                plot_list.append({
                    'x': [str(xi) for xi in x] if x_to_string else x,
                    'y': [str(yi) for yi in y] if y_to_string else y,
                    'name': group,
                    'type': plot_type,
                    'legendgroup': group,
                    'marker': {'color': colours[i]}
                })
        else:
            x, y = _flatten_(data)
            plot_list = [{
                    'x': [str(xi) for xi in x] if x_to_string else x,
                    'y': y,
                    'type': plot_type,
                    'marker': {'color': DEFAULT_COLOUR}
            }]
        return plot_list
    elif isinstance(data, dict):
        plotly_format = {
            lclass: _df_to_plotly_dict_(class_data)
            for lclass, class_data in sorted(data.items())
        }
        # computing layout
        layout = _subplot_layout_(plotly_format)
        # computing actual plots
        plotly_subplots = []
        for i, (lclass, plotly_data) in enumerate(plotly_format.items()):
            for tmp_data in plotly_data:
                tmp_data['xaxis'] = f'x{i + 1}'
                tmp_data['yaxis'] = f'y{i + 1}'
                tmp_data['title'] = lclass
                tmp_data['showlegend'] = i == 0
                plotly_subplots.append(tmp_data)
        return plotly_subplots, layout


def _df_to_plotly_heatmap_(
    data: Union[pd.DataFrame, np.ndarray],
    index: pd.Index = None, columns: pd.Index = None,
    scale: Tuple[int, int] = (5, 35),
    extrema: Tuple[float, float] = None, **kwargs
) -> Dict[str, Any]:
    zero_mask = data != 0
    if extrema is None:
        scaled_values = np.array(data) / (np.nanmax(data) - np.nanmin(data)[zero_mask])
    else:
        scaled_values = np.array(data) / (extrema[1] - extrema[0])
    scaled_values = scaled_values * (scale[1] - scale[0]) + scale[0]
    if isinstance(data, np.ndarray):
        if index is None:
            raise ValueError("'index' must be given, when numpy array is given")
        if columns is None:
            raise ValueError("'index' must be given, when numpy array is given")
        zero_mask = zero_mask.flatten()
        text = [f'Concentration: {value}' for i, value in enumerate(data.flatten())
                if zero_mask[i]]
    else:
        index = data.index
        columns = data.columns
        zero_mask = zero_mask.values.flatten()
        text = [f'Concentration: {value}' for i, value in enumerate(data.values.flatten())
                if zero_mask[i]]
    x, y = [], []
    x = data.shape[0] * list(columns)
    for i in range(data.shape[0]):
        y += data.shape[1] * [index[i]]
    scaled_values = list(scaled_values.flatten()[zero_mask])
    return {
        'x': [str(xi) for xi in np.array(x)[zero_mask]],
        'y': [str(yi) for yi in np.array(y)[zero_mask]],
        'marker': {
            'size': scaled_values,
            'color': kwargs.pop('color', DEFAULT_COLOUR),
            'line': {'width': 0}
        },
        'type': kwargs.pop('type', 'heatmap'),
        'text': text,
        **kwargs
    }


def _plotly_c_vs_db_(
    data: Dict[str, Union[Dict[str, pd.DataFrame], pd.DataFrame]],
    with_groups: bool = True, alpha: float = 1, **kwargs
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if with_groups:
        min_ = np.nanmin([np.nanmin(x) for class_data in data.values() for x in class_data.values()])
        max_ = np.nanmax([np.nanmax(x) for class_data in data.values() for x in class_data.values()])
    else:
        min_ = np.nanmin([np.nanmin(x) for x in data.values()])
        max_ = np.nanmax([np.nanmax(x) for x in data.values()])
    plots = {}
    for i, (lclass, class_data) in enumerate(sorted(data.items())):
        if with_groups:
            colours = _get_colours_(len(class_data))
            for j, (group, group_data) in enumerate(sorted(class_data.items())):
                # TODO: add scatter offset per group
                pt_form = _df_to_plotly_heatmap_(
                    group_data, type='scatter',
                    color=colours[j],
                    legendgroup=group, extrema=(min_, max_),
                    mode='markers', name=group,
                    opacity=alpha,
                    # boxpoints='all',
                    # hoveron='points', pointpos=0,
                    # boxmode='group', line={'color': 'rgba(0,0,0,0)'},
                    # fillcolor='rgba(0,0,0,0)'
                )
                pt_form['xaxis'] = f'x{i + 1}'
                pt_form['yaxis'] = f'y{i + 1}'
                if i == 0:
                    pt_form['title'] = lclass
                    pt_form['showlegend'] = True
                else:
                    pt_form['showlegend'] = False
                plots.setdefault(lclass, []).append(pt_form)
        else:
            plots[lclass] = [
                _df_to_plotly_heatmap_(class_data, type='scatter', extrema=(min_, max_))
            ]
    return [plot_data for plot in plots.values() for plot_data in plot], _subplot_layout_(plots, **kwargs)


def _per_sample_sums_(
    data: pd.DataFrame, lipid_map: Dict[str, List[Lipid]],
    groups: pd.Series = None
) -> Dict[str, Union[Dict[str, pd.Series], Dict[str, Dict[str, pd.Series]]]]:
    # data: lipids in columns
    classes = {}
    lengths = {}
    dbs = {}
    for lipid_class, lipids in lipid_map.items():
        classes[lipid_class] = [lipid.get_dataname() for lipid in lipids]
        for lipid in lipids:
            lengths.setdefault(lipid.sum_length(), []).append(lipid.get_dataname())
            dbs.setdefault(lipid.sum_dbs(), []).append(lipid.get_dataname())
    class_data = {lclass: data.loc[lipids, :] for lclass, lipids in classes.items()}
    sums = {
        'Lipid Class': {},
        'Sum Length': {},
        'Sum DB': {},
        'C vs DB': {}
    }
    for lclass, lclass_data in class_data.items():
        sums['Lipid Class'][lclass] = lclass_data.sum(axis=0)
        sums['Sum Length'][lclass] = {
            llength: lclass_data.loc[set(lipids).intersection(lclass_data.index), :].sum(axis=0)
            for llength, lipids in lengths.items()
        }
        sums['Sum DB'][lclass] = {
            ldb: lclass_data.loc[set(lipids).intersection(lclass_data.index), :].sum(axis=0)
            for ldb, lipids in dbs.items()
        }
        if groups is None:
            sums['C vs DB'][lclass] = {
                llength: {
                    ldb: lclass_data.loc[
                            set(c_lipids).intersection(db_lipids).intersection(lclass_data.index), :
                         ].sum(axis=0).mean()
                    for ldb, db_lipids in dbs.items()
                } for llength, c_lipids in lengths.items()
            }
        else:
            unique_groups = groups.unique()
            sums['C vs DB'][lclass] = {
                group: {
                    llength: {
                        ldb: lclass_data.loc[
                                set(c_lipids).intersection(db_lipids).intersection(lclass_data.index), groups == group
                             ].sum(axis=0).mean()
                        for ldb, db_lipids in dbs.items()
                    } for llength, c_lipids in lengths.items()
                } for group in unique_groups
            }
    return sums


def lipidome_summary(
    self, as_dict: bool = False, **kwargs
) -> Union[Tuple[pd.DataFrame, dict, dict, dict], Tuple[list, tuple, tuple, tuple]]:
    """
    TODO
    :param self:
    :param as_dict:
    :return:
    """
    sum_data = _per_sample_sums_(self.data, self.gln.get_lipid_dict(), self.groups)
    class_sums = pd.DataFrame(sum_data['Lipid Class'])
    # normalise by total class content
    length_summary = {
        lclass: (pd.DataFrame(sum_length).T / class_sums[lclass]).T
        for lclass, sum_length in sum_data['Sum Length'].items()
    }
    db_summary = {
        lclass: (pd.DataFrame(sum_db).T / class_sums[lclass]).T
        for lclass, sum_db in sum_data['Sum DB'].items()
    }
    class_summary = (class_sums.T / class_sums.sum(axis=1)).T

    if self.groups is not None:
        # Group assignment
        class_summary['Group'] = self.groups
        length_summary = {lclass: sum_length.assign(Group=self.groups)
                          for lclass, sum_length in length_summary.items()}
        # x/y-axis: C/DB, value: (per group) mean
        class_sums['Group'] = self.groups
        class_means = class_sums.groupby('Group').mean()
        c_db_scatter = {
            lclass: {
                group: pd.DataFrame.from_dict(group_data) / class_means.loc[group, lclass]
                for group, group_data in c_db.items()
            } for lclass, c_db in sum_data['C vs DB'].items()
        }
        db_summary = {lclass: db_length.assign(Group=self.groups)
                      for lclass, db_length in db_summary.items()}
        with_groups = True
    else:
        with_groups = False
        # x/y-axis: C/DB, value: mean
        class_means = class_sums.mean(axis=0, skipna=True)
        c_db_scatter = {lclass: pd.DataFrame.from_dict(c_db) / class_means[lclass]
                        for lclass, c_db in sum_data['C vs DB'].items()}
    if as_dict:
        return _df_to_plotly_dict_(class_summary), \
               _df_to_plotly_dict_(length_summary), \
               _df_to_plotly_dict_(db_summary), \
               _plotly_c_vs_db_(c_db_scatter, with_groups, xaxis={'title': 'Sum Length'},
                                yaxis={'title': 'Sum DBs'}, **kwargs)
    return class_summary, length_summary, db_summary, c_db_scatter


def _z_score_(data: np.ndarray) -> np.ndarray:
    return ((data.T - np.nanmean(data, axis=1)) / np.nanstd(data, axis=1)).T


def substructure_selection(
    self, functions: list, **kwargs
) -> Tuple[pd.DataFrame, Union[pd.Series, pd.DataFrame]]:
    """
    TODO
    :param self:
    :param functions:
    :param kwargs:
    :return:
    """
    if self.groups is None:
        # TODO unsupervised group assignment
        raise ValueError('groups have to be given for feature selection')
    ohencoded = False
    if np.issubdtype(self.groups.dtype, np.number):
        groups = self.groups
    else:
        ohencoded = True
        groups = pd.get_dummies(self.groups)
    substructure_data = analysis_lipid_substructure(
        self, functions,
        single_n_combination=kwargs.pop('single_n_combionations', True),
        feature_combinations=kwargs.pop('feature_combinations', len(functions)),
        **kwargs
    )
    substructure_data = pd.DataFrame(substructure_data.values,
                                     index=substructure_data.index,
                                     columns=substructure_data.columns)
    # TODO: elastic net or similar?
    model = LinearRegression()
    substructs = substructure_data.replace([np.inf, -np.inf], np.nan).fillna(0)
    model.fit(substructs.values.T, groups.values)
    # TODO: add some prediction plot?
    if isinstance(groups, pd.Series):
        return substructure_data, pd.Series(model.coef_, substructure_data.index).sort_values(ascending=False)
    else:
        return substructure_data, pd.DataFrame(model.coef_, index=groups.columns, columns=substructure_data.index)


def plot_pca(
    data, groups: pd.Series = None,
    to_plotly: bool = False, title: str = '',
    ax: Optional[plt.axis] = None, scale: bool = True
) -> Union[Tuple[List[Dict[str, Dict[str, Any]]], Dict[str, Any]], plt.axis]:
    """
    TODO
    :param data:
    :param groups:
    :param to_plotly:
    :param title:
    :param ax:
    :param scale:
    :return:
    """
    pca = PCA(n_components=2)
    is_df = False
    if isinstance(data, pd.DataFrame):
        is_df = True
        if scale:
            scaled = _z_score_(data.values)
            scaled[np.isnan(scaled)] = 0
            scaled[np.isinf(data)] = 0
            embedding = pca.fit_transform(scaled.T)
        else:
            embedding = pca.fit_transform(data.replace([np.inf, -np.inf], np.nan).fillna(0).T)
    else:
        data_ = data.copy()
        data_[np.isinf(data)] = 0
        data_[np.isnan(data)] = 0
        if scale:
            data_ = _z_score_(data_)
        embedding = pca.fit_transform(data_.T)
    if to_plotly:
        layout = {
            'xaxis': {'title': f'PC1 ({round(100 * pca.explained_variance_ratio_[0], ndigits=2)}%)'},
            'yaxis': {'title': f'PC2 ({round(100 * pca.explained_variance_ratio_[1], ndigits=2)}%)'},
            'title': title
        }
        if groups is not None:
            unique_groups = groups.unique()
            colours = _get_colours_(unique_groups.size)
            plot_data = [
                {
                    'x': list(embedding[groups[data.columns] == group, 0]),
                    'y': list(embedding[groups[data.columns] == group, 1]),
                    'type': 'scatter',
                    'name': group,
                    'mode': 'markers',
                    'text': data.columns.to_list() if is_df else [],
                    'markers': {'color': colours[i]}
                }
                for i, group in enumerate(sorted(unique_groups))
            ]
        else:
            plot_data = [
                {
                    'x': list(embedding[:, 0]),
                    'y': list(embedding[:, 1]),
                    'type': 'scatter',
                    'mode': 'markers',
                    'text': data.columns.to_list() if is_df else []
                }
            ]
        return plot_data, layout
    # TODO: plot with matplotlib
    if ax is None:
        fig, ax = plt.subplots()
    if groups is not None:
        unique_groups = groups.unique()
        colours = _get_colours_(unique_groups.size)
        for i, group in enumerate(sorted(unique_groups)):
            ax.scatter(
                embedding[groups[data.columns] == group, 0],
                embedding[groups[data.columns] == group, 1],
                label=group, c=colours[i]
            )
    else:
        ax.scatter(
            embedding[:, 0],
            embedding[:, 1]
        )
    ax.set_xlabel(f'PC1 ({round(100 * pca.explained_variance_ratio_[0], ndigits=2)}%)')
    ax.set_ylabel(f'PC2 ({round(100 * pca.explained_variance_ratio_[1], ndigits=2)}%)')
    return ax


def plot_heatmap(
    data, scale: bool = True,
    groups: pd.Series = None,
    to_plotly: bool = False, title: str = '',
    ax: Optional[plt.axis] = None
) -> Union[Dict[str, Any], sns.matrix.ClusterGrid]:
    """
    TODO
    :param data:
    :param scale:
    :param groups:
    :param to_plotly:
    :param title:
    :param ax:
    :return:
    """
    if scale:
        plot_data = _scale_(data.values)
    else:
        plot_data = data.values
    if groups is not None:
        unique_groups = groups.unique()
        group_colours = dict(zip(unique_groups, _get_colours_(unique_groups.size)))
        column_colours = groups[plot_data.columns].map(group_colours)
    if to_plotly:
        raise NotImplementedError("'to_plotly' currently not implemented for 'plot_heatmap'")
        # TODO: dendrogram/clustering order (columns) and column annotation
        # if groups is not None:
        #     return _df_to_plotly_heatmap_(plot_data, data.index, data.columns, title=title)
        # else:
        #     return _df_to_plotly_heatmap_(plot_data, data.index, data.columns, title=title)
    plot_data = pd.DataFrame(plot_data, index=data.index, columns=data.columns)
    if groups is not None:
        return sns.clustermap(plot_data, column_colors=column_colours, ax=ax)
    else:
        return sns.clustermap(plot_data, ax=ax)
