from typing import Dict, Tuple, List, Union
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import itertools
import re

# From package
from .reaction_types import L_FAmodify
from .edgelist import enzyme_str
from .libAP_nx import LSOprimizer, flatten, convergence_plot
from .utils import plot_networks, compute_ratios, plot_lineplot, plot_histogram, plot_boxplot


def analysis_reaction_network_enrichment(self,
                                         group1: str,
                                         group2: str,
                                         difference_as_change: bool = True,
                                         penalty_fa_reaction: float = 1,
                                         penalty_n_reactions: float = .2,
                                         default_ratio: float = 0,
                                         min_size: int = 5,
                                         max_size: int = 20,
                                         max_iter: int = 100,
                                         temp: float = 20,
                                         repetitions: int = 5,
                                         opt_max: bool = True,
                                         recompute_edgelist: bool = False,
                                         p_value_iterations: int = 10000,
                                         plot_scores: bool = True,
                                         plot_n_col: int = 3,
                                         plot_fig_size: Tuple[int, int] = (10, 18),
                                         plot_hspace: float = 0.4,
                                         correct_n_lipids: bool = True
                                         ) -> Tuple[Dict[str, nx.Graph],
                                                    Dict[str, List[float]],
                                                    Dict[str, float],
                                                    plt.Figure]:
    if not hasattr(self, "groups") or self.groups is None:
        raise AttributeError("Analysis only possible with group labels.")

    if (group2 not in self.groups.values) or (group1 not in self.groups.values):
        raise ValueError("Both given groups must be in the groups.")

    if group1 == group2:
        raise ValueError("Both groups have the same group name.")

    g, l_mapping = self.gln.native_network(filter_duplicates=False,
                                           excluded_reaction_types=None,
                                           return_lipid_mapping=True,
                                           bipartite=False,
                                           # bipartite_type='hyper',
                                           recompute_edgelist=recompute_edgelist,
                                           multi=True  # Necessary for correct hypergraph conversion
                                           )

    # Get data & lipid to data mapping
    user_data = self.data.T
    reverse_mapping = {
        net_name: data_name for data_name, net_names in l_mapping.items()
        for net_name in net_names
    }

    # ##############
    # ANALYSIS START------------------------------------------------------------------------------------------------
    # ##############
    print("Analysis start")

    # 1. Get all reaction IDs & edges with attributes---------------------------------------------------------------
    reaction_ids: Dict[str, List[List[Union[str, Dict]]]] = {}
    for ed in g.edges:
        tmp_edge_data = g.get_edge_data(*ed)
        if tmp_edge_data["reaction_id"] in reaction_ids.keys():
            reaction_ids[tmp_edge_data["reaction_id"]].append([ed[0], ed[1], tmp_edge_data])
        else:
            reaction_ids[tmp_edge_data["reaction_id"]] = [[ed[0], ed[1], tmp_edge_data]]

    print("Computing objectives")
    # 2. Compute ratio differences----------------------------------------------------------------------------------
    new_reaction_node_dict: Dict[str, List[Union[List[str], float]]] = {}

    for r_id, el in reaction_ids.items():
        # 2.1. Only one Edge -> Ratio or Penalty
        if len(el) == 1:
            nel = el[0]
            # 2.1.1. Penalty
            if nel[2]['reaction_type'] == L_FAmodify:
                new_reaction_node_dict[r_id] = [[nel[0], nel[1]], -penalty_fa_reaction, [nel[0], nel[1]]]
            # 2.1.2. Ratio
            else:
                tmp_ed = [reverse_mapping[nel[0]], reverse_mapping[nel[1]]]
                if difference_as_change:
                    tmp_ratio = user_data[tmp_ed[0]] - user_data[tmp_ed[1]]
                else:
                    tmp_ratio = user_data[tmp_ed[0]] / user_data[tmp_ed[1]]

                # Join with group labels
                tmp_ratio_df = pd.DataFrame({"r": tmp_ratio}).join(pd.DataFrame({"groups": self.groups}))

                # Series with groups
                tmp_series = tmp_ratio_df.groupby("groups").mean(numeric_only=True)["r"]
                if tmp_series[group1] == 0:
                    val = 0
                else:
                    val = abs((tmp_series[group1] - tmp_series[group2]) / tmp_series[group1])
                if val is np.nan or pd.isna(val):
                    val = default_ratio
                new_reaction_node_dict[r_id] = [[nel[0], nel[1], enzyme_str + nel[2]["enzyme_id"]], val,
                                                [nel[0], nel[1]]]
        # 2.2. More edges -> 1,2 or 2,2 reaction where partners need to be figured out
        elif len(el) == 2:
            nel0 = el[0]
            nel1 = el[1]
            substrates = []
            products = []
            if nel0[2]['l1_type'] == 'substrate':
                substrates.append(nel0[0])
                products.append(nel0[1])
            else:
                substrates.append(nel0[1])
                products.append(nel0[0])
            if nel1[2]['l1_type'] == 'substrate':
                substrates.append(nel1[0])
                products.append(nel1[1])
            else:
                substrates.append(nel1[1])
                products.append(nel1[0])
            mapped_substrates = list(set([reverse_mapping[x] for x in substrates]))
            mapped_products = list(set([reverse_mapping[x] for x in products]))

            if difference_as_change:
                if correct_n_lipids:
                    tmp_ratio = np.mean([user_data[x] for x in mapped_products], axis=0) - np.mean(
                        [user_data[x] for x in mapped_substrates], axis=0)
                    tmp_ratio = pd.Series(tmp_ratio, index=user_data[mapped_products[0]].index)
                else:
                    tmp_ratio = sum([user_data[x] for x in mapped_products]) - sum(
                        [user_data[x] for x in mapped_substrates])
            else:
                if correct_n_lipids:
                    product_prod = math.prod([user_data[x] for x in mapped_substrates]) ** (1 / len(mapped_substrates))
                    substrate_prod = math.prod([user_data[x] for x in mapped_products]) ** (1 / len(mapped_products))
                    tmp_ratio = product_prod / substrate_prod
                else:
                    tmp_ratio = math.prod([user_data[x] for x in mapped_products]) / \
                                math.prod([user_data[x] for x in mapped_substrates])

            # Join with group labels
            tmp_ratio_df = pd.DataFrame({"r": tmp_ratio}).join(pd.DataFrame({"groups": self.groups}))

            # Series with groups
            tmp_series = tmp_ratio_df.groupby("groups").mean(numeric_only=True)["r"]
            if tmp_series[group1] == 0:
                val = 0
            else:
                val = abs((tmp_series[group1] - tmp_series[group2]) / tmp_series[group1])
            if val is np.nan or pd.isna(val):
                val = default_ratio
            ids = flatten([substrates, products, [enzyme_str + nel0[2]["enzyme_id"]]])
            new_reaction_node_dict[r_id] = [list(set(ids)), val, flatten([substrates, products])]

        else:
            raise ValueError("More edges than expected occurred per reaction. Please contact the developer")
    # 3. Build & reconnect network----------------------------------------------------------------------------------
    print("Building & reconnecting network")

    # Prepare nodes
    new_node_list = []
    node_set = dict()
    counter = 0
    for n, v in new_reaction_node_dict.items():
        if str(sorted(v[2])) not in node_set.keys():
            new_node_list.append((n, {'org_nodes': v[0], 'objective': v[1], 'enzymes': [x for x in v[0] if
                                                                                        x.startswith(enzyme_str)],
                                      'lipid_nodes': v[2]}))
            node_set[str(sorted(v[2]))] = counter
            counter += 1
        else:
            new_node_list[node_set[str(sorted(v[2]))]][1]['org_nodes'] += [x for x in v[0] if x.startswith(enzyme_str)]
            new_node_list[node_set[str(sorted(v[2]))]][1]['enzymes'] += [x for x in v[0] if x.startswith(enzyme_str)]

    # Make bipartite graph
    B = nx.Graph()
    B.add_nodes_from(new_node_list, bipartite=0)
    B.add_nodes_from(list(g.nodes), bipartite=1)  # Lipids
    enz_l = []
    for i in new_node_list:
        if len(i[1]['enzymes']) > 0:
            enz_l += i[1]['enzymes']
    B.add_nodes_from(list(set(enz_l)), bipartite=1)  # Enzymes

    new_edgelist = []
    for i in new_node_list:
        for j in i[1]['org_nodes']:
            new_edgelist.append((i[0], j))
    B.add_edges_from(new_edgelist)  # Edges between reactions and Lipids/Enzymes

    # Project back to reaction network
    top_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
    # bottom_nodes, _ = bipartite.sets(B)
    G = bipartite.projected_graph(B, top_nodes)

    # # Make edges
    # new_edgelist = set()
    # for nn1 in range(len(new_node_list)):
    #     for nn2 in range(nn1, len(new_node_list)):
    #         if nn1 != nn2:
    #             # share lipids or reactions make an edge
    #             if len(set(new_node_list[nn1][1]['org_nodes']).intersection(new_node_list[nn2][1]['org_nodes'])) > 0:
    #                 new_edgelist.add((new_node_list[nn1][0], new_node_list[nn2][0]))

    gn = nx.Graph()                  # Reaction graph
    gn.add_nodes_from(new_node_list)
    gn.add_edges_from(list(G.edges))
    # gn.add_edges_from(new_edgelist)

    # 4. Local search-----------------------------------------------------------------------------------------------
    print("Local search")
    gh, l_mapping = self.gln.native_network(filter_duplicates=False,
                                            excluded_reaction_types=None,
                                            return_lipid_mapping=True,
                                            bipartite=True,
                                            bipartite_type='hyper',
                                            recompute_edgelist=recompute_edgelist
                                            )
    results = {}
    scores = {}
    p_values = {}
    for c in nx.connected_components(gn):
        if len(c) > max_size:
            cg = gn.subgraph(c).copy()
            sc = -100000
            nodes = []
            c_scores = []
            for rep in range(repetitions):
                print("Local search repetition:", rep)
                opt = LSOprimizer(G=cg,
                                  L_min=min_size,
                                  L_max=max_size,
                                  max_iter=max_iter,
                                  reaction_penalty=penalty_n_reactions,
                                  T=temp,
                                  verbose=False,
                                  node_scoring=True,
                                  plot=False)
                tmp_nodes, tmp_sc, tmp_c_scores = opt.run_ls()
                if tmp_sc > sc:
                    print(f"Improved to {tmp_sc}")
                    sc = tmp_sc
                    nodes = tmp_nodes
                    c_scores = tmp_c_scores

            if opt_max:
                print("Rerunning local search on best result")
                opt = LSOprimizer(G=cg,
                                  L_min=min_size,
                                  L_max=max_size,
                                  max_iter=max_iter,
                                  reaction_penalty=penalty_n_reactions,
                                  T=temp,
                                  verbose=False,
                                  node_scoring=True,
                                  seed=nodes,
                                  plot=False)
                tmp_nodes, tmp_sc, tmp_c_scores = opt.run_ls()
                if tmp_sc > sc:
                    print(f"Improved to {tmp_sc}")
                    sc = tmp_sc
                    nodes = tmp_nodes
                    c_scores = c_scores + tmp_c_scores
            if plot_scores:
                convergence_plot(c_scores)
            # Transform back to original graph
            tmp_na = dict(gn.nodes(data='org_nodes'))
            transformed_nodes = list(set(flatten([tmp_na[x] for x in nodes])))
            g_small = nx.subgraph(gh, transformed_nodes)

            title = f'Connected component {len(results)}'
            results[title] = g_small
            scores[title] = c_scores

            # 5. Compute empirical p-value for result ------------------------------------------------------------------
            print("Computing p-value")
            tmp_seed_score = []
            for p_iter in range(p_value_iterations):
                n_sample_nodes = np.random.choice(np.arange(min_size, max_size+1), 1)[0]
                tmp_seed_nodes = np.random.choice(list(new_reaction_node_dict.keys()), n_sample_nodes, replace=False)
                tmp_score = [new_reaction_node_dict[key][1] for key in tmp_seed_nodes if
                                                new_reaction_node_dict[key][1] != -penalty_fa_reaction]
                if len(tmp_score) > 0:
                    tmp_seed_score.append(np.mean(tmp_score))
                else:
                    tmp_seed_score.append(0)
            p_values[title] = float(np.sum(np.array(tmp_seed_score) > sc)) / p_value_iterations

    results, fig = plot_networks(
        networks=results,
        scores=scores,
        p_values=p_values,
        plot_n_col=plot_n_col,
        plot_fig_size=plot_fig_size,
        plot_hspace=plot_hspace
    )

    return results, scores, p_values, fig


def analysis_ratio_network_enrichment(self,
                                      group1: str,
                                      group2: str,
                                      data_is_log: bool = True,
                                      penalty_fa_reaction: float = 1,
                                      penalty_n_reactions: float = 1,
                                      default_ratio: float = 0,
                                      min_size: int = 5,
                                      max_size: int = 20,
                                      max_iter: int = 100,
                                      temp: float = 20,
                                      recompute_edgelist: bool = False,
                                      hyper: bool = False) -> List[nx.Graph]:

    if not hasattr(self, "groups") or self.groups is None:
        raise AttributeError("Analysis only possible with group labels.")

    if (group2 not in self.groups.values) or (group1 not in self.groups.values):
        raise ValueError("Both given groups must be in the groups.")

    if hyper:
        g, l_mapping = self.gln.native_network(filter_duplicates=False,
                                               excluded_reaction_types=None,
                                               return_lipid_mapping=True,
                                               bipartite=True,
                                               bipartite_type='hyper',
                                               recompute_edgelist=recompute_edgelist
                                               )
    else:
        g, l_mapping = self.gln.native_network(filter_duplicates=False,
                                               excluded_reaction_types=None,
                                               return_lipid_mapping=True,
                                               bipartite=False,
                                               recompute_edgelist=recompute_edgelist
                                               )

    user_data = self.data.T
    reverse_mapping = {
        net_name: data_name for data_name, net_names in l_mapping.items()
        for net_name in net_names
    }

    # Compute ratios
    for ed in g.edges:
        tmp_edge_data = g.get_edge_data(*ed)
        # print(ed[1])
        if (tmp_edge_data['reaction_type'] != L_FAmodify) and ((not ed[1].startswith(enzyme_str)) and
                                                               (not ed[0].startswith(enzyme_str))):
            tmp_ed = [reverse_mapping[ed[0]], reverse_mapping[ed[1]]]
            if data_is_log:
                tmp_ratio = user_data[tmp_ed[0]] - user_data[tmp_ed[1]]
            else:
                tmp_ratio = user_data[tmp_ed[0]] / user_data[tmp_ed[1]]

            # Join with group labels
            tmp_ratio_df = pd.DataFrame({"r": tmp_ratio}).join(pd.DataFrame({"groups": self.groups}))

            # Series with groups
            tmp_series = tmp_ratio_df.groupby("groups").mean(numeric_only=True)["r"]
            val = abs((tmp_series[group1] - tmp_series[group2]) / tmp_series[group1])
            if val is np.nan or pd.isna(val):
                val = default_ratio
            g.edges[ed[0], ed[1]]["objective"] = val

        elif tmp_edge_data['reaction_type'] == L_FAmodify and ((not ed[1].startswith(enzyme_str)) and
                                                               (not ed[0].startswith(enzyme_str))):
            # Reaction which will be penalized
            g.edges[ed[0], ed[1]]["objective"] = - penalty_fa_reaction

        else:
            g.edges[ed[0], ed[1]]["objective"] = 0

    if hyper:  # Local search not yet implemented for hyper
        return [g]
    # Local search
    results = []
    for c in nx.connected_components(g):
        if len(c) > max_size:
            cg = g.subgraph(c).copy()
            opt = LSOprimizer(G=cg,
                              L_min=min_size,
                              L_max=max_size,
                              max_iter=max_iter,
                              reaction_penalty=penalty_n_reactions,
                              T=temp,
                              verbose=False)
            nodes, sc = opt.run_ls()
            g_small = nx.subgraph(g, nodes)

            pos = nx.spring_layout(g_small)
            labels = nx.get_edge_attributes(g_small, 'objective')
            for key in labels:
                labels[key] = np.round(labels[key], 2)
            nx.draw_networkx(g_small, pos, font_size=8)

            nx.draw_networkx_edge_labels(g_small, pos, edge_labels=labels)
            plt.title(f'connected component {len(results)}, score {np.round(sc, 3)}')
            plt.show()

            results.append(g_small)

    return results


def _extract_reactions_(
    network: nx.Graph, edge_attr: str
) -> Tuple[List[str], Dict[str, str]]:
    unique_enzyme_list = []
    enzyme_structure_dict = {}
    for ed in network.edges:
        tmp_edge_data = network.get_edge_data(*ed)
        if tmp_edge_data['reaction_type'] != L_FAmodify:
            if tmp_edge_data[edge_attr] not in unique_enzyme_list:
                unique_enzyme_list.append(tmp_edge_data[edge_attr])
                if tmp_edge_data["reaction_structure"] == "1,1":
                    enzyme_structure_dict[tmp_edge_data[edge_attr]] = tmp_edge_data["reaction_structure"]
                else:
                    enzyme_structure_dict[tmp_edge_data[edge_attr]] = tmp_edge_data["reaction_structure"] + \
                                                                      ";" + tmp_edge_data['reaction_type']
    return unique_enzyme_list, enzyme_structure_dict


def _ratio_distributions_(
    self,
    network: nx.Graph,
    name_map: Dict[str, List[str]],
    enzyme_subset: Union[None, List] = None,
    difference_as_change: bool = True,
    distribution_per_sample: bool = True,
    select_groups: List[str] = None,
    fa_specific: bool = False,
    plot_n_col: int = 3,
    plot_fig_size: Tuple[int, int] = (20, 20),
    plot_hspace: float = 0.4,
    difference_dist: bool = False,
    reference_group: str = "",
    as_boxplot: bool = False,
    as_subplots: bool = True,
    z_scores: bool = False
) -> Tuple[plt.Figure, Dict[str, pd.DataFrame]]:
    # Extract all reactions classes for reaction_type != L_FAmodify (only class reactions)
    if fa_specific:
        edge_attr = "id_fa_raw"
    else:
        edge_attr = "enzyme_id"

    unique_enzyme_list, enzyme_structure_dict = _extract_reactions_(network, edge_attr)

    print(f"Identified {len(unique_enzyme_list)} reaction classes for which ratio distribution analysis "
          f"will be performed.")

    if len(unique_enzyme_list) == 0:
        raise ValueError("No class reactions could be identified, cannot perform ratio distribution analysis.")

    user_data = self.data.T
    reverse_mapping = {
        net_name: data_name for data_name, net_names in name_map.items()
        for net_name in net_names
    }
    # removing enzymes if enzyme subset is given
    if enzyme_subset is not None:
        enzyme_subset = {enzyme.split('Enzyme: ')[1] for enzyme in enzyme_subset}
        unique_enzyme_list = list(set(unique_enzyme_list).intersection(enzyme_subset))
        enzyme_structure_dict = {enzyme: enzyme_structure_dict[enzyme] for enzyme in unique_enzyme_list}

    # Compute ratios for all reaction classes -> per sample and per reaction
    # TODO:
    # * 2,2 & 1,2 reactions using reaction_structure and l1/l2_type attributes
    # * for 2,2 L_HG the set_id has to be considered to make two sets
    df_dict = compute_ratios(unique_enzyme_list=unique_enzyme_list,
                             enzyme_structure_dict=enzyme_structure_dict,
                             gr=network,
                             reverse_mapping=reverse_mapping,
                             difference_as_change=difference_as_change,
                             user_data=user_data,
                             class_reactions=self.gln.get_class_reactions(),
                             edge_attr=edge_attr)

    # Prepare data for histogram
    # If groups are given, then add those to the df
    # The ratios should be in the column "value" and potential groups in column "groups"
    if hasattr(self, "groups") and self.groups is not None:
        if distribution_per_sample:
            data_for_hist = {key: df.melt(ignore_index=False).join(
                pd.DataFrame({"groups": self.groups})).reset_index() for key, df in df_dict.items()}

            if select_groups is not None:
                data_for_hist = {key: df[df["groups"].isin(select_groups)] for key, df in data_for_hist.items()}
        else:
            data_for_hist = {key: df.join(
                pd.DataFrame({"groups": self.groups})).groupby(
                "groups").mean(numeric_only=True).melt(
                ignore_index=False).reset_index() for key, df in df_dict.items()}

            if difference_dist:
                tmp_dict = dict()
                for reac, dat in data_for_hist.items():
                    ref_dat = dat[dat['groups'] == reference_group].set_index('variable')
                    oth_dat = dat[dat['groups'] != reference_group].set_index('variable')
                    tmp_dat = ref_dat.join(oth_dat, how='left', lsuffix="_l", rsuffix="_r")
                    tmp_dat = tmp_dat.assign(**{
                        "value": (tmp_dat['value_r'] - tmp_dat['value_l']) / abs(tmp_dat['value_l'])
                    }).reset_index().rename(columns={"groups_r": "groups"})
                    tmp_dict[reac] = tmp_dat
                data_for_hist = tmp_dict

            if select_groups is not None:
                data_for_hist = {key: df[df["groups"].isin(select_groups)] for key, df in data_for_hist.items()}
    else:
        if distribution_per_sample:
            data_for_hist = {key: df.melt(ignore_index=False) for key, df in df_dict.items()}
        else:
            data_for_hist = {key: pd.DataFrame({"value": df.mean(numeric_only=True)}) for key, df in
                             df_dict.items()}
    if as_boxplot:
        fig = plot_boxplot(data_for_hist,
                           plot_n_col=plot_n_col,
                           plot_fig_size=plot_fig_size,
                           plot_hspace=plot_hspace,
                           difference_dist=difference_dist,
                           as_subplots=as_subplots,
                           z_scores=z_scores)
    else:
        fig = plot_histogram(data_for_hist,
                             plot_n_col=plot_n_col,
                             plot_fig_size=plot_fig_size,
                             plot_hspace=plot_hspace,
                             difference_dist=difference_dist)

    # TODO: 4. Distribution deconvolution

    return fig, data_for_hist


def analysis_ratio_distribution(self,
                                enzyme_subset: List = None,
                                difference_as_change: bool = True,
                                distribution_per_sample: bool = True,
                                select_groups: List[str] = None,
                                fa_specific: bool = False,
                                plot_n_col: int = 3,
                                plot_fig_size: Tuple[int, int] = (20, 20),
                                plot_hspace: float = 0.4,
                                difference_dist: bool = False,
                                reference_group: str = "",
                                as_boxplot: bool = False,
                                as_subplots: bool = True,
                                z_scores: bool = False) -> Tuple[plt.Figure, Dict[str, pd.DataFrame]]:
    """
    TODO: Tim
    :param enzyme_subset: list, default None, if given only reactions with the given enzymes are plotted
    :param difference_as_change: boolean, default True, to compute the difference or the quotient between substrates and products
    :param distribution_per_sample: boolean, default True, whether to plot distribution for each sample or cumulated
    :param select_groups: list, default None, list of groups to consider in the analysis
    :param fa_specific: boolean, default False, whether to compute ratios fatty acid specific
    :param plot_n_col: int, default 3, number of subplots per row
    :param plot_fig_size: Tuple[int, int], default (20, 20), total figure size
    :param plot_hspace: float, default 0.4, horizontal spacing between subplots
    :param difference_dist: boolean, default False, whether to plot the difference of group distributions or the
                            distributions per group
    :param reference_group: str, default '',
    :param as_boxplot: boolean, default False, whether to plot ratios as boxplots or histograms (if False)
    :param as_subplots: boolean default True, if False and as_boxplot is True all reactions will be plotted in a
                        single plot with one reaction per position on the x-axis
    :param z_scores: boolean, default False, whether to scale ratios to zero mean and unit variance (over all groups)
    :return: 2-tuple, plt.Figure containing histograms and a dictionary of data frames containing ratio distributions
    """
    if (not hasattr(self, "groups") or self.groups is None) and difference_dist:
        raise AttributeError("Analysis with difference_dist=True only possible with group labels.")

    if difference_dist and (reference_group not in self.groups.values):
        raise ValueError("Reference group must be in the groups.")
    # Recompute network (native, bipartite=False)
    print("Recomputing native network (This will not overwrite your last computed network).")
    g, l_mapping = self.gln.native_network(filter_duplicates=False,
                                           excluded_reaction_types=None,
                                           return_lipid_mapping=True,
                                           bipartite=False,
                                           multi=True
                                           )
    return _ratio_distributions_(
        self, g, l_mapping, enzyme_subset,
        difference_as_change, distribution_per_sample, select_groups,
        fa_specific, plot_n_col, plot_fig_size, plot_hspace,
        difference_dist, reference_group, as_boxplot, as_subplots,
        z_scores=z_scores
    )


def analysis_enrichment_ratio_plots(
    self,
    enrichment_network: nx.Graph,
    difference_as_change: bool = True,
    distribution_per_sample: bool = True,
    select_groups: List[str] = None,
    fa_specific: bool = False,
    plot_n_col: int = 3,
    plot_fig_size: Tuple[int, int] = (20, 20),
    plot_hspace: float = 0.4,
    difference_dist: bool = False,
    reference_group: str = "",
    as_boxplot: bool = False,
    as_subplots: bool = True,
    z_scores: bool = True
) -> Tuple[plt.Figure, Dict[str, pd.DataFrame]]:
    """
    :param enrichment_network: nx.Graph, enriched subnetwork as returned by
                               `LipidNetwork.analysis_reaction_network_enrichment`
    :param difference_as_change: boolean, default True, to compute the difference or the quotient between substrates and products
    :param distribution_per_sample: boolean, default True, whether to plot distribution for each sample or cumulated
    :param select_groups: list, default None, list of groups to consider in the analysis
    :param fa_specific: boolean, default False, whether to compute ratios fatty acid specific
    :param plot_n_col: int, default 3, number of subplots per row
    :param plot_fig_size: Tuple[int, int], default (20, 20), total figure size
    :param plot_hspace: float, default 0.4, horizontal spacing between subplots
    :param difference_dist: boolean, default False, whether to plot the difference of group distributions or the
                            distributions per group
    :param reference_group: str, default '',
    :param as_boxplot: boolean, default False, whether to plot ratios as boxplots or histograms (if False)
    :param as_subplots: boolean default True, if False and as_boxplot is True all reactions will be plotted in a
                        single plot with one reaction per position on the x-axis
    :param z_scores: boolean, default False, whether to scale ratios to zero mean and unit variance (over all groups)
    :return: 2-tuple, plt.Figure containing histograms and a dictionary of data frames containing ratio distributions
    """
    if (not hasattr(self, "groups") or self.groups is None) and difference_dist:
        raise AttributeError("Analysis with difference_dist=True only possible with group labels.")
    if difference_dist and (reference_group not in self.groups.values):
        raise ValueError("Reference group must be in the groups.")
    print("Computing native network. This will not overwrite your previously computed network")
    native_net, lipid_mapping = self.gln.native_network(
        filter_duplicates=False,
        excluded_reaction_types=None,
        return_lipid_mapping=True,
        bipartite=False
    )

    direct_edges = [edge for edge in enrichment_network.edges
                    if edge in native_net.edges and
                    f"Enzyme: {native_net.edges[edge]['enzyme_id']}" in enrichment_network.nodes]
    cleaned_network = enrichment_network.edge_subgraph(direct_edges)
    return _ratio_distributions_(
        self, cleaned_network, lipid_mapping, None,
        difference_as_change, distribution_per_sample, select_groups,
        fa_specific, plot_n_col, plot_fig_size, plot_hspace,
        difference_dist, reference_group, as_boxplot, as_subplots,
        z_scores=z_scores
    )


def analysis_chain_length(self,
                          control_condition: str,
                          other_groups: List[str] = None,
                          lipid_classes: List[str] = None,
                          data_is_log: bool = False,
                          return_data: bool = False,
                          **kwargs
                          ) -> Union[plt.Figure, Dict[str, pd.DataFrame]]:
    """
    TODO
    :param self:
    :param control_condition:
    :param other_groups:
    :param lipid_classes:
    :param data_is_log:
    :param return_data:
    :param kwargs:
    :return:
    """
    if not hasattr(self, "groups"):
        raise AttributeError("Data groups must be available for fold change Analysis")

    # Set lipid weights
    lipid_dict = self._get_weighted_lipid_dict()
    if lipid_classes is None:
        lipid_classes = lipid_dict.keys()
    feature_matrix = self.data.T.drop(self.data.T.index.values)

    for cls in lipid_dict.keys():
        if cls in lipid_classes:
            for lip in lipid_dict[cls]:

                # Get class & length
                tmp_feature = lip.get_lipid_class() + ": " + str(lip.sum_length())

                # Add row, if feature not yet in:
                if tmp_feature not in feature_matrix.index.values:
                    feature_matrix = feature_matrix.append(pd.Series([0] * feature_matrix.shape[1],
                                                                     index=feature_matrix.columns,
                                                                     name=tmp_feature))

                feature_matrix.loc[tmp_feature, lip.get_dataname()] += (1 / lip.get_div_factor())

    new_df = feature_matrix.dot(self.data).T

    classes = list(set([x.split(": ")[0] for x in new_df.columns.values]))

    # Get sub df only for one class
    df_list = {}

    for cls in sorted(classes):
        df_list[cls] = new_df[[col for col in new_df if col.startswith(f'{cls}:')]].copy()
        df_list[cls] = df_list[cls].rename(columns={col: col.split(": ")[1] for col in df_list[cls].columns.values})
        joined_df = df_list[cls].join(pd.DataFrame({"groups": self.groups}))
        control_df = joined_df[joined_df["groups"] == control_condition]
        control_mean = pd.DataFrame({"val": control_df.mean(axis=0,
                                                            numeric_only=True)}).reset_index().rename(
            columns={"index": "variable"})

        if other_groups is not None:
            other_df = joined_df[joined_df["groups"].isin(other_groups)].groupby("groups").mean().melt(
                ignore_index=False).reset_index()
        else:
            other_df = joined_df[joined_df["groups"] != control_condition].groupby("groups").mean().melt(
                # old:  != control_condition
                ignore_index=False).reset_index()
        other_df = other_df.set_index('variable').join(control_mean.set_index('variable')).reset_index()
        if data_is_log:
            other_df["FC"] = other_df["value"] - other_df["val"]
        else:
            other_df["FC"] = other_df["value"] / other_df["val"]

        df_list[cls] = other_df

    if return_data:
        return df_list
    res = plot_lineplot(df_list, **kwargs)
    return res


def analysis_lipid_substructure(self, combined: bool = False) -> pd.DataFrame:
    """
    TODO: Tim

    Parameters
    ----------
    :param combined: bool, default=False
        Combine newly generated lipid substructures with the original lipid data and
        output the combined data frame.

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
            tmp_features.append(lip.get_category())
            # *backbone
            tmp_features.append(lip.get_backbone())
            # *headgroup
            tmp_features.append(lip.get_headgroup())
            # *class
            tmp_features.append(lip.get_lipid_class())
            # *fatty acids
            # **single
            for i in lip.get_fas():
                tmp_features.append(f"FA: {str(i)}")
            # **combined -> for now only pairwise
            if len(lip.get_fas()) >= 2:
                for x in itertools.combinations(lip.get_fas(), 2):
                    tmp_features.append(f"FA: {str(sorted(x))}")

            # 1. Single features
            for feat in tmp_features:
                # Add row, if feature not yet in:
                if feat not in feature_matrix.index.values:
                    feature_matrix = feature_matrix.append(pd.Series([0] * feature_matrix.shape[1],
                                                                     index=feature_matrix.columns,
                                                                     name=feat))

                feature_matrix.loc[feat, lip.get_dataname()] += (1 / lip.get_div_factor())

            # 2. Combined features
            for x in itertools.combinations(tmp_features, 2):
                combined_feature = str(sorted(x))
                if len(re.findall("FA", combined_feature)) < 2:
                    if combined_feature not in feature_matrix.index.values:
                        feature_matrix = feature_matrix.append(pd.Series([0] * feature_matrix.shape[1],
                                                                         index=feature_matrix.columns,
                                                                         name=combined_feature))

                    feature_matrix.loc[combined_feature, lip.get_dataname()] += (1 / lip.get_div_factor())
    if combined:
        return feature_matrix.dot(self.data).append(self.data)
    else:
        return feature_matrix.dot(self.data)

