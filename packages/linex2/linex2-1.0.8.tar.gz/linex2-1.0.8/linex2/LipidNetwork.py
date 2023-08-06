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

import warnings
import re
from typing import List, Dict, Tuple, Union, Callable, Any, Set
from itertools import permutations, combinations
from warnings import warn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colorbar import Colorbar
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, to_hex, to_rgba
import networkx as nx
import networkx.drawing.layout as nx_layout
from pyvis.network import Network
import json

# From package
from .GenerateLipidNetwork import GenerateLipidNetwork
from .parser import (
    parse_fa_reactions,
    parse_fatty_acids,
    parse_excluded_fa_reactions,
    parse_lipid_list
)
from .reference import parse_lipid_reference_table, parse_lipid_reference_table_dict, ReferenceLipid
from .tmp_dirty_functions import (
    make_organism_reaction_list_from_reactome,
    make_all_reaction_list_from_reactome,
    make_all_reaction_list_from_rhea
)
from .lipid import Lipid
from .colour_helper import _generate_colormap_
from .utils import (
    unique_elements,
    SymmetricMatrix,
    extend_class_fa,
    check_databases,
    combine_reactions
)
from .misc import _range_scale_, _size_legend_, _tuple_to_string_, _get_sizes_report_nas_
from .exceptions import NotComputedError, InputDataError
from .vis_utils import VisParser, DynamicVisParser, STATIC_EDGE_PROPERTIES, STATIC_NODE_PROPERTIES
from . import templates
from .load_data import *

with pkg_resources.path(templates, "lipid_colours.json") as path:
    LIPID_CLASS_COLOURS = json.load(open(path, "r"))


class LipidNetwork:
    __slots__ = [
        "gln",
        "layout",
        "network",
        "lipid_mapping",
        "reverse_mapping",
        "last_network_call",
        "_attributes_to_plot",
        "lipid_attributes",
        "interaction_attributes",
        "node_colours",
        "edge_colours",
        "data",
        "groups",
        "unique_groups",
        "comparisons",
        "directed",
        "_ref_dict",
        "_incompatible_lipids"
    ]

    network: nx.Graph
    layout: Dict[str, np.ndarray]

    data: pd.DataFrame
    groups: pd.Series
    unique_groups: pd.Series
    comparisons: List[Tuple[str, str]]

    lipid_attributes: Union[Dict[str, Dict[str, Any]], Dict[str, Dict[Union[str, Tuple[str, str]], Dict[str, Any]]]]
    interaction_attributes: Union[
        Dict[str, SymmetricMatrix], Dict[str, Dict[Union[str, Tuple[str, str]], SymmetricMatrix]]]
    node_colours: Dict[Union[str, Tuple[str, str]], Tuple[Union[dict, Dict[str, Union[str, Any]]], list]]
    edge_colours: Dict[Union[str, Tuple[str, str]], Tuple[Union[dict, Dict[str, Union[str, Any]]], list]]
    _attributes_to_plot: Dict[str, Set[str]]

    gln: GenerateLipidNetwork
    _incompatible_lipids: List[str]

    lipid_mapping: Dict[str, List[str]]
    reverse_mapping: Dict[str, str]
    last_network_call: Dict[str, any]

    directed: bool

    # database related slots
    _ref_dict: Dict[str, ReferenceLipid]

    _allowed_node_attributes_ = {
        "lipid_class", "c_index", "db_index", "oh_index",
        "chain_length", "desaturation", "hydroxylation",
        "nlog_pvalues", "fold_changes", "degree",
        "betweenness", "closeness"
    }

    _allowed_edge_attributes_ = {
        "correlations",
        "partial_correlations",
        "reaction_type",
        "enzyme_id",
        "correlation_changes",
        "partial_correlation_changes",
        "enzyme_gene_name",
        "enzyme_uniprot"
    }
    # auxiliary attributes
    _attr_group_size_ = {
        # edge attributes
        "correlations": 1,
        "partial_correlations": 1,
        "reaction_type": 0,
        "enzyme_id": 0,
        "correlation_changes": 2,
        "partial_correlation_changes": 2,
        # node attributes
        "fold_changes": 2,
        "pvalues": 2,
        "nlog_pvalues": 2,
        "lipid_class": 0,
        "c_index": 0,
        "db_index": 0,
        "oh_index": 0,
        "desaturation": 0,
        "hydroxylation": 0,
        "chain_length": 0,
        "closeness": 0,
        "betweenness": 0,
        "degree": 0
    }
    _discrete_map_ = {
        # node features
        "lipid_class": True,
        "c_index": False,
        "db_index": False,
        "oh_index": False,
        "desaturation": False,
        "hydroxylation": False,
        "degree": False,
        "betweenness": False,
        "closeness": False,
        "chain_length": False,
        "fold_changes": False,
        "pvalues": False,
        "nlog_pvalues": False,
        # edge features
        "correlations": False,
        "partial_correlations": False,
        "correlation_changes": True,
        "partial_correlation_changes": True,
        "reaction_type": True
    }

    # Imported methods -------------------------------------------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    from ._network_analysis import (
        analysis_reaction_network_enrichment,
        analysis_ratio_network_enrichment,
        analysis_ratio_distribution,
        analysis_enrichment_ratio_plots,
        analysis_chain_length
    )
    # noinspection PyUnresolvedReferences
    from ._network_compute_statistics import (
        compute_correlations,
        compute_pvalues,
        compute_fold_changes,
        compute_correlation_changes,
        compute_partial_correlations,
        _correlation_computation_
    )
    # noinspection PyUnresolvedReferences
    from ._network_lipid_utils import (
        _get_weighted_lipid_dict,
        add_lipid,
        all_lipid_objects,
        all_native_lipids,
        get_incompatible_lipids,
        all_molecular_species_lipids
    )
    # noinspection PyUnresolvedReferences
    from ._network_lipidome_summary import (
        analysis_lipid_substructure,
        lipidome_summary,
        # TODO: add substructure selection including plotting
        substructure_selection
    )
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(
        self,
        data: Union[str, pd.DataFrame],
        fatty_acids: str = "",
        groups: Union[str, pd.Series] = None,
        lipids_are_columns: bool = True,
        node_attributes: List[str] = None,
        edge_attributes: List[str] = None,
        lipids_lm_compatible: bool = False,
        organism: str = "HSA",
        database: Union[str, List[str], Tuple[str]] = ("Rhea", "Reactome"),
        ether_conversions: bool = True,
        confirmed_lipid_species: str = ""
    ):
        """

        Parameters
        ----------
        :param data : Union[str, pd.DataFrame]
            Path to a csv file that can be read with
            pandas.read_csv or pd.DataFrame

        :param fatty_acids: str, default=""
            Path to a txt file containing fatty acid
            settings in the form described on the
            LINEX homepage. If "", a default fatty acid file is used.

        :param groups: pandas.Series or str, optional
            Sample groups as a pandas.Series or a path to file
            which contains the sample groups.
            Series indices should correspond the columns of 'data'.

        :param lipids_are_columns: bool, default=True
            If True in the "data" table, lipids represent columns and samples, rows.
            If False, lipids are rows and samples columns.

        :param node_attributes: List[str], optional
            List of node attributes to be made available for plotting. Calling
            LipidNetwork.add_attributes_to_plot has the same effect. For a list
            of available options call linex2.node_colour_options

        :param edge_attributes: List[str], optional
            List of edge attributes to be made available for plotting. Calling
            LipidNetwork.add_attributes_to_plot has the same effect. For a list
            of available options call linex2.edge_colour_options

        :param lipids_lm_compatible: bool, default=False
            When the lipids in the data file are not compatible with the LIPID MAPS nomenclature,
            they can be converted with LipidLynxX. If the parameter is False,
            lipids will be converted before (This can take up to several minutes).
            If True, the lipids won't be converted.
            For more information visit the LipidLynxX website: https://www.lipidmaps.org/lipidlynxx/

        :param organism: str, default="HSA"
            Three letter organism code.
            We use reactions from the Reactome database, where an organism has to be selected.
            All available organisms can be found here: https://reactome.org/content/schema/objects/Species
            The default organism is Homo Sapiens. If the user provides an empty string "" all reactions from the
            database are considered.

        :param database:  Union[str, List[str], Tuple[str]], default = ("Rhea", "Reactome")
            Lipid reaction networks can be computed from the Reactome and Rhea database.
            Reactome is organism specific, Rhea does not provide this information.
            One or both databases can be selected and the network is
            computed using the reactions from those databases.

        :param ether_conversions: bool, default=True
            Include Conversions of Lipids to ether lipids in the network as L_FAmodify edges.
        """

        # Get reference lipids
        self._ref_dict = parse_lipid_reference_table_dict(STANDARD_LIPID_CLASSES)

        # Read data if necessary
        if isinstance(data, pd.DataFrame):
            user_data = data
        elif isinstance(data, str):
            user_data = pd.read_csv(data, index_col=0)
        else:
            raise ValueError("Data must be a str (path to data file) or pd.DataFrame")

        # Transpose, so that lipids are columns
        if not lipids_are_columns:
            user_data = user_data.T

        # Extract lipids
        data_lipids = user_data.columns.values
        if all([isinstance(lipid, int) for lipid in data_lipids]):
            raise ValueError(
                'Lipid axis names contain integers only. '
                'Did you forget to transpose your data or add the right column names?'
            )

        # Parse lipids
        lipid_dict, converted_names_mapping, incompatible_lipids = parse_lipid_list(data_lipids,
                                                                                    reference_lipids=self._ref_dict,
                                                                                    ll_compatible=lipids_lm_compatible)
        incompatible_2 = []
        lipid_dict_confirmed = dict()
        # Get confirmed species
        if confirmed_lipid_species != "":
            confirmed_species_file = open(confirmed_lipid_species, "r")
            confirmed_lines = [line.strip() for line in confirmed_species_file]
            lipid_dict_confirmed, _, incompatible_2 = parse_lipid_list(confirmed_lines,
                                                                       reference_lipids=self._ref_dict,
                                                                       ll_compatible=lipids_lm_compatible)

        # Check if enough lipids
        if len(incompatible_lipids) >= (len(data_lipids) - 2):
            raise InputDataError(f"Only {len(data_lipids) - len(incompatible_lipids)} lipids were identified "
                                 f"successfully. At least 3 lipids have to be identified to use LINEX2.")

        # Remove incompatible lipids
        user_data = user_data.drop(columns=incompatible_lipids + incompatible_2)

        self._incompatible_lipids = incompatible_lipids + incompatible_2  # save them for later access

        # Rename lipids with new names
        user_data = user_data.rename(columns=converted_names_mapping)

        # Uebergibt lipid_dict
        self._compute_gln_(
            lipid_dict=lipid_dict,
            fa_file=fatty_acids,
            organism=organism,
            database=database,
            ether_conversions=ether_conversions,
            confirmed_species_dict = lipid_dict_confirmed
        )

        self._set_data_groups_(user_data.T, groups)  # Forward transposed user_data
        self.last_network_call = {}
        self.network = None

        # 'static' properties (i.e. data-indepentent)
        # these do NOT include graph metrics!
        self._attributes_to_plot = {
            "nodes": STATIC_NODE_PROPERTIES.union(self._allowed_node_attributes_),
            "edges": STATIC_EDGE_PROPERTIES.union(self._allowed_edge_attributes_)
        }
        self._reset_nodes_()
        self._reset_edges_()

        # adding the data-dependent attributes to plot
        self.add_attributes_to_plot(node_attributes, edge_attributes)

    def _compute_gln_(self, lipid_dict: Dict[str, List[Lipid]],
                      fa_file: str,
                      organism: str = "HSA",
                      database: Union[str, List[str], Tuple[str]] = ("Rhea", "Reactome"),
                      ether_conversions: bool = True,
                      confirmed_species_dict: Dict[str, List[Lipid]] = None
                      ):
        """
        ** Function for internal use only! **

        Build the GenerateLipidNetwork class with.

        :param lipid_dict:  Dict[str, List[Lipid]]
            Dict of parsed lipids from the data.
            Is computed e.g. from the function parse_lipid_list

        :param fa_file:
            Path to fatty acid file.

        :param organism: str, default="HSA"
            Three letter organism code.
            We use reactions from the Reactome database, where an organism has to be selected.
            All available organisms can be found here: https://reactome.org/content/schema/objects/Species
            The default organism is Homo Sapiens. If the user provides an empty string "" all reactions from the
            database are considered.

        :param database:  Union[str, List[str], Tuple[str]], default = ("Rhea", "Reactome")
            Lipid reaction networks can be computed from the Reactome and Rhea database.
            Reactome is organism specific, Rhea does not provide this information.
            One or both databases can be selected and the network is
            computed using the reactions from those databases.

        :return:
            Initializes slot: LipidNetwork.gln
        """
        if confirmed_species_dict is None:
            confirmed_species_dict = dict()

        ref_lips = parse_lipid_reference_table(STANDARD_LIPID_CLASSES)
        # del ref_dict["Cholesterol"]
        # del ref_dict["ST"]

        # Extract possible class reactions
        if isinstance(database, str):
            database = [database]

        if check_databases(database):  # Raises Error, if database not valid
            pass

        class_reaction_list = []
        if "Reactome" in database:
            if organism == "":
                class_reaction_list.append(make_all_reaction_list_from_reactome(REACTOME_OTHERS_UNIQUE,
                                                                                REACTOME_REACTION_CURATION,
                                                                                REACTOME_REACTION_TO_MOLECULE,
                                                                                self._ref_dict,
                                                                                REACTOME_REACTION_DETAILS,
                                                                                verbose=False)[0]
                                           )
            else:
                class_reaction_list.append(make_organism_reaction_list_from_reactome(REACTOME_OTHERS_UNIQUE,
                                                                                     REACTOME_REACTION_CURATION,
                                                                                     REACTOME_REACTION_TO_MOLECULE,
                                                                                     self._ref_dict,
                                                                                     REACTOME_REACTION_DETAILS,
                                                                                     verbose=False,
                                                                                     organism=organism)
                                           )

        if "Rhea" in database:
            class_reaction_list.append(make_all_reaction_list_from_rhea(RHEA_OTHERS_UNIQUE,
                                                                        RHEA_REACTION_CURATION,
                                                                        RHEA_REACTION_TO_MOLECULE,
                                                                        self._ref_dict,
                                                                        gn_mapping=RHEA_MAPPING,
                                                                        verbose=False)[0]
                                       )

        if len(class_reaction_list) == 1:
            # If only one database is used, the Reaction list can be used as is.
            class_reacs = class_reaction_list[0]
        else:
            # If both databases are used, they are combined.
            class_reacs = combine_reactions(class_reaction_list[0],
                                            class_reaction_list[1])

        # Parse fatty acid file
        if fa_file == "":
            with pkg_resources.path(data, "default_fatty_acids.txt") as path:
                fatty_acid_file = open(path, "r")
        else:
            fatty_acid_file = open(fa_file, "r")

        fa_lines = [line for line in fatty_acid_file]
        fa_reacs = parse_fa_reactions(fa_lines)
        # print(fa_reacs)
        ex_fa_reacs = parse_excluded_fa_reactions(fa_lines)
        class_fas = parse_fatty_acids(fa_lines)
        # Extend class fatty acids
        class_fas = extend_class_fa(class_fa=class_fas, lipid_dict=lipid_dict, add_to_all=True)
        self.gln = GenerateLipidNetwork(ref_lips, lipid_dict, class_reacs,
                                        fa_reacs, ex_fa_reacs, class_fas, ether_conversions=ether_conversions,
                                        confirmed_species_dict=confirmed_species_dict)

    def _update_attrs_to_plot_(self, attr: str, nodes: bool):
        type_ = "nodes" if nodes else "edges"
        allowed = self._allowed_node_attributes_ if nodes else self._allowed_edge_attributes_
        if attr in allowed:
            self._attributes_to_plot[type_].add(attr)

    def add_attributes_to_plot(
        self, node_attributes: List[str] = None,
        edge_attributes: List[str] = None
    ):
        if node_attributes is not None:
            for attr in self._attributes_to_plot["nodes"]:
                self._update_attrs_to_plot_(attr, True)
        if edge_attributes is not None:
            for attr in self._attributes_to_plot["edges"]:
                self._update_attrs_to_plot_(attr, False)

    def _reset_nodes_(self, reset_colours=True):
        # TODO: add colour only for the single added node => speed-up
        #       and expand this to other options once they are available
        if not hasattr(self, "lipid_attributes"):
            self.lipid_attributes = {}
        if self.network is not None:
            for attr in self._attributes_to_plot["nodes"]:
                if self._attr_group_size_[attr] == 0:
                    net_attr = nx.get_node_attributes(self.network, attr)
                    if net_attr:
                        self.lipid_attributes[attr] = net_attr
        if reset_colours:
            self.node_colours = {}

    def _reset_edges_(self, reset_colours=True):
        self.last_network_call = {}
        self.interaction_attributes = {
            attr: {} for attr in self._attributes_to_plot["edges"]
        }
        if reset_colours:
            self.edge_colours = {}

    # Excluded for now, since the data is necessary for parsing the lipids in the __init__ function.
    # def add_data(self, data: Union[pd.DataFrame, str]):
    #     self._set_data_groups_(data=data, groups=None)
    #
    # def add_groups(self, groups: Union[pd.Series, str]):
    #     self._set_data_groups_(data=None, groups=groups)

    def _check_data_(self, check_groups=True):
        if not hasattr(self, "data"):
            raise ValueError("p-values cannot be computed when no dataset is given. Please call 'add_data'")
        elif self.data is None:
            raise ValueError("p-values cannot be computed when no dataset is given. Please call 'add_data'")
        if check_groups:
            if not hasattr(self, "groups"):
                raise ValueError("p-values cannot be computed when no groups are given. Please call 'add_groups'")
            elif self.groups is None:
                raise ValueError("p-values cannot be computed when no groups are given. Please call 'add_groups'")

    def _set_data_groups_(self, data: Union[pd.DataFrame, str] = None,
                          groups: Union[pd.Series, str] = None):
        # TODO: adapt once species strings are converted
        #       to Lipid objects internally to match names
        if data is not None:
            if hasattr(self, "data"):
                warn("'data' has already been set, skipping...")
            elif isinstance(data, pd.DataFrame):
                self.data = data
            elif isinstance(data, str):
                self._set_data_groups_(data=pd.read_csv(data, index_col=0))
            else:
                raise ValueError(
                    f"'data' must be str or pd.DataFrame, not {type(data).__name__}"
                )
            # NOTE: we force column names to be strings in order
            #       to avoid mismatching due to different data types
            self.data.columns = self.data.columns.astype(str)
        if groups is not None:
            if hasattr(self, "groups") and self.groups is not None:
                warn("'groups' has already been set, skipping...")
            elif isinstance(groups, pd.Series):
                self.groups = groups
            elif isinstance(groups, str):
                self.groups = pd.Series(pd.read_csv(groups, index_col=0))
                if hasattr(self, "data"):
                    matched = np.isin(self.data.columns, self.groups.index)
                    if not matched.all():
                        raise InputDataError(
                            f"Samples '{self.data.columns[~matched]}' were not found in group annotation"
                        )
            else:
                raise ValueError(
                    f"'groups' must be str or pd.Series, not {type(groups).__name__}"
                )
            # NOTE: we force the index to be strings in order
            #       to avoid mismatching due to different data types
            self.groups.index = self.groups.index.astype(str)
            self.groups = self.groups.astype(str)
            try:
                self.groups = self.groups[self.data.columns]
            except KeyError:
                matched = np.isin(self.data.columns, self.groups.index)
                raise InputDataError(
                    f"Samples '{self.data.columns[~matched]}' were not found in group annotation"
                )
            # unique groups
            self.unique_groups = self.groups.unique()
            # all pairwise combinations of unique groups
            self.comparisons = list(combinations(self.unique_groups, 2))

        elif not hasattr(self, "groups"):
            self.groups = None

    def _compute_network_(
        self, network: str,
        filter_duplicates: bool = False,
        excluded_reaction_types: List[str] = None,
        bipartite: bool = False,
        bipartite_type: str = "enzyme",
        verbose: bool = False,
        force_overwrite: bool = False
    ):
        # TODO: rewrite this to adapt to new layout
        function_call = locals()
        _ = function_call.pop('self')
        if function_call == self.last_network_call and not force_overwrite:
            if verbose:
                warnings.warn(f"Current call '{function_call}' is equivalent to existing network.")
            return
        else:
            self.last_network_call = function_call
            if verbose:
                print(f"Function call: {function_call}")
        if network == "native":
            self.network, self.lipid_mapping = self.gln.native_network(
                filter_duplicates=filter_duplicates,
                excluded_reaction_types=excluded_reaction_types,
                return_lipid_mapping=True,
                bipartite=bipartite,
                bipartite_type=bipartite_type
            )
        else:
            self.network, self.lipid_mapping = self.gln.molecular_species_network(
                filter_duplicates=filter_duplicates,
                excluded_reaction_types=excluded_reaction_types,
                return_lipid_mapping=True,
                bipartite=bipartite,
                bipartite_type=bipartite_type
            )
        self.reverse_mapping = {
            net_name: data_name for data_name, net_names in self.lipid_mapping.items()
            for net_name in net_names
        }
        self._reset_nodes_(False)
        self.lipid_attributes["degree"] = dict(self.network.degree())
        self.lipid_attributes["betweenness"] = nx.betweenness_centrality(self.network)
        self.lipid_attributes["closeness"] = nx.closeness_centrality(self.network)
        # setting data independent attributes
        for node_attr in self._attributes_to_plot["nodes"]:
            if self._attr_group_size_[node_attr] == 0:
                self._generate_node_colours(
                    node_attr, self._discrete_map_[node_attr]
                )
        # reaction types and enzymes
        for attr in ["reaction_type", "enzyme_id"]:
            rts = pd.DataFrame(index=list(self.network.nodes), columns=list(self.network.nodes))
            for edge, rt in nx.get_edge_attributes(self.network, attr).items():
                rts.loc[edge[0], edge[1]] = rt
                rts.loc[edge[1], edge[0]] = rt
            self.interaction_attributes[attr] = SymmetricMatrix(rts)

    def compute_native_network(
        self, filter_duplicates: bool = False,
        excluded_reaction_types: List[str] = None,
        bipartite: bool = False,
        bipartite_type: str = "enzyme",
        **kwargs
    ):
        # TODO: adapt documentation
        """
        Computing the native (i.e. mixed species level) network

        Parameters
        ----------
        :param filter_duplicates : bool, optional, default True
            Whether duplicate edges should be removed.

        :param excluded_reaction_types : list, optional, default None
            Optional list of reaction types, that should be ignored when
            computing the network edges.
        """
        self._compute_network_(
            "native", filter_duplicates=filter_duplicates,
            excluded_reaction_types=excluded_reaction_types,
            bipartite=bipartite,
            bipartite_type=bipartite_type,
            **kwargs
        )

    def compute_molecular_network(
        self, filter_duplicates: bool = False,
        excluded_reaction_types: List[str] = None,
        bipartite: bool = False,
        bipartite_type: str = "enzyme",
        **kwargs
    ):
        # TODO: adapt documentation
        """
        Computing the molecular species network

        Parameters
        ----------
        :param filter_duplicates : bool, optional, default True
            Whether duplicate edges should be removed

        :param excluded_reaction_types : list, optional, default None
            Optional list of reaction types, that should be ignored when
            computing the network edges
        """
        self._compute_network_(
            "molecular", filter_duplicates=filter_duplicates,
            excluded_reaction_types=excluded_reaction_types,
            bipartite=bipartite,
            bipartite_type=bipartite_type,
            **kwargs
        )

    def add_network_visualisation(self):
        # TODO: add a check for bipartite
        for attr in self._attributes_to_plot["nodes"]:
            self._add_network_attribute_(attr)
        for attr in self._attributes_to_plot["edges"]:
            self._add_network_attribute_(attr, False)

    def _check_attributes_(self,
                           edge_colour_attr: Union[str, None],
                           node_colour_attr: Union[str, None]):
        """
        Auxiliary Function to check if edge and node colouring attributes have been
        computed previously

        Parameters
        ----------
        :param edge_colour_attr : str
            String indicating the attribute used for edge colouring.

        :param node_colour_attr :
            String indicating the attribute used for node colouring.
        """
        edge_colour_attr_ = {
            "correlations": "compute_correlations",
            "partial_correlations": "compute_partial_correlations",
            "correlation_changes": "compute_correlation_changes",
            "partial_correlation_changes": "compute_correlation_changes",
            "reaction_type": "",
        }
        node_colour_attr_ = {
            "fold_changes": "compute_fold_changes",
            "pvalues": "compute_pvalues",
            "nlog_pvalues": "compute_pvalues",
            "lipid_class": None,
            "c_index": None,
            "db_index": None,
            "oh_index": None,
            "chain_length": None,
            "desaturation": None,
            "hydroxylation": None,
            "closeness": None,
            "betweenness": None,
            "degree": None
        }

        not_in = "'{0}' must be one of {1}, not {2}"

        if edge_colour_attr is not None:
            if (edge_colour_attr not in edge_colour_attr_.keys() and
                edge_colour_attr not in self._allowed_edge_attributes_):
                raise ValueError(
                    not_in.format("edge_colour_attr", list(edge_colour_attr_.keys()),
                                  edge_colour_attr)
                )

            if edge_colour_attr != "reaction_type":
                if self.interaction_attributes is not None:
                    if (edge_colour_attr not in self.interaction_attributes.keys() and
                        not nx.get_edge_attributes(self.network, edge_colour_attr)):
                        raise NotComputedError(edge_colour_attr, edge_colour_attr_[edge_colour_attr])
                    elif (not self.interaction_attributes.get(edge_colour_attr) and
                          not nx.get_edge_attributes(self.network, edge_colour_attr)):
                        raise NotComputedError(edge_colour_attr, edge_colour_attr_[edge_colour_attr])
                else:
                    raise NotComputedError(edge_colour_attr, edge_colour_attr_[edge_colour_attr])
        if node_colour_attr is not None:
            if (node_colour_attr not in node_colour_attr_.keys() and
                node_colour_attr not in self._allowed_node_attributes_):
                raise ValueError(
                    not_in.format("node_colour_attr", list(node_colour_attr_.keys()),
                                  node_colour_attr)
                )
            if self.lipid_attributes is not None:
                if (not self.lipid_attributes.get(node_colour_attr) and
                    not nx.get_edge_attributes(self.network, edge_colour_attr)):
                    raise NotComputedError(node_colour_attr, node_colour_attr_[node_colour_attr])
            else:
                raise NotComputedError(node_colour_attr, node_colour_attr_[node_colour_attr])

    def _add_network_attribute_(
        self, attr: str, nodes: bool = True,
        group_subset: Union[tuple, list, set] = None,
        overwrite: bool = True, add_group: bool = True,
        from_group: bool = True
    ):
        if nodes:
            if not self.lipid_attributes.get(attr, {}):
                raise NotComputedError(
                    f"{attr} has not been found in the list of computed "
                    "lipid properties. Please call the appropriate function first!"
                )
        else:
            if not self.interaction_attributes.get(attr):
                raise NotComputedError(
                    f"{attr} has not been found in the list of computed "
                    "interaction properties. Please call the appropriate function first!"
                )

        if self.network is None:
            raise ValueError(
                "No network has been computed yet! Please do so and call this function again."
            )
        if not overwrite:
            if nodes:
                old = nx.get_node_attributes(self.network, attr)
            else:
                old = nx.get_edge_attributes(self.network, attr)
            if old is not None:
                if not isinstance(old, dict):
                    return
                # some attributes are dicts => need to check whether
                # they are empty
                if old:
                    return

        attr_size = self._attr_group_size_[attr]
        if self.groups is not None:
            if attr_size > 0:
                # checking if correct number of groups are provided
                # if no groups are provided but the number of unique
                # groups in self are the same as the number of groups
                # required for the respective attribute, they are used
                if group_subset is None:
                    if self.unique_groups.size == attr_size:
                        group_subset = self.unique_groups
                    else:
                        raise ValueError(
                            f"'{attr}' requires exactly {attr_size} groups, "
                            f"but {self.unique_groups.size} are specified in the class instance. "
                            "Please use 'group_subset' to specify a subset of groups."
                        )
                elif len(group_subset) != attr_size:
                    raise ValueError(
                        f"'{attr}' requires exactly {attr_size} groups, "
                        f"but {len(group_subset)} are given."
                    )
                # actual computations with the correct number of groups
                if len(group_subset) == 1:
                    group = group_subset[0]
                    if add_group:
                        attr_ = f"{attr}_{group}"
                    else:
                        attr_ = attr
                    if nodes:
                        if not nx.get_node_attributes(self.network, attr_):
                            for node in self.network.nodes:
                                self.network.nodes[node][attr_] = {}
                        for node in self.network.nodes:
                            node_name = node if attr in STATIC_NODE_PROPERTIES else self.reverse_mapping.get(node)
                            if add_group:
                                to_add = self.lipid_attributes[attr][group].get(node_name)
                            else:
                                to_add = self.lipid_attributes[attr].get(node_name)
                            if to_add is None and attr not in STATIC_NODE_PROPERTIES:
                                if node_name in self.data.index:
                                    # in this case the attribute should have been computed
                                    raise ValueError(
                                        f"Something went wrong while computing {attr}. "
                                        f"{node} is present in input data frame, but not in attribute values"
                                    )
                                else:
                                    # this means the node was added during network generation
                                    # and does not have any associated values
                                    # TODO: adapt this behaviour when parsing is all set up!
                                    to_add = np.nan
                            if hasattr(to_add, "item"):
                                # json.serialize cannot handle numpy data types
                                to_add = to_add.item()
                            if add_group:
                                self.network.nodes[node][attr_] = to_add
                            else:
                                self.network.nodes[node][attr][group] = to_add
                    else:
                        if not nx.get_edge_attributes(self.network, attr_):
                            for edge in self.network.edges:
                                self.network.edges[edge][attr_] = {}
                        for edge in self.network.edges:
                            if attr not in STATIC_EDGE_PROPERTIES:
                                edge_name = (self.reverse_mapping.get(edge[0]),
                                             self.reverse_mapping.get(edge[1]))
                            else:
                                edge_name = edge
                            if from_group:
                                to_add = self.interaction_attributes[attr][group].get(edge_name[0], edge_name[1])
                            else:
                                to_add = self.interaction_attributes[attr].get(edge_name[0], edge_name[1])
                            if to_add is None and attr not in STATIC_EDGE_PROPERTIES:
                                # TODO: adapt when parsing is all set up!
                                if edge_name[0] in self.data.index and edge_name[1] in self.data.index:
                                    raise ValueError(
                                        f"Something went wrong while computing {attr}. "
                                        f"{edge[0]} and {edge[1]} are present in input data frame, but not in attribute values"
                                    )
                                else:
                                    to_add = np.nan
                            if hasattr(to_add, "item"):
                                # json.serialize cannot handle numpy data types
                                to_add = to_add.item()
                            if add_group:
                                self.network.edges[edge][attr_] = to_add
                            else:
                                self.network.edges[edge][attr][group] = to_add
                else:
                    # NOTE: only 1 or 2 possible (no more groups allowed)
                    # => would work for more than 2 groups as well!
                    attr_computed = False
                    for perm in permutations(group_subset):
                        if nodes:
                            if self.lipid_attributes[attr].get(perm) is not None:
                                attr_computed = True
                                break
                        else:
                            if self.interaction_attributes[attr].get(perm) is not None:
                                attr_computed = True
                                break
                    if not attr_computed:
                        raise NotComputedError(attr, group_subset, for_subset=True)
                    group = tuple(group_subset)
                    if group is None:
                        raise ValueError(
                            "Groups in 'group_subset' are not matching the group "
                            "group names provided in the class instance."
                        )
                    if add_group:
                        attr_ = f"{attr}_{_tuple_to_string_(group)}"
                    else:
                        attr_ = attr
                    if nodes:
                        nx.set_node_attributes(self.network,
                                               self.gln.n_lipids * [""],
                                               name=attr_)
                        for node in self.network.nodes:
                            node_name = node if attr in STATIC_NODE_PROPERTIES else self.reverse_mapping.get(node)
                            if from_group:
                                to_add = self.lipid_attributes[attr][group].get(node_name)
                            else:
                                to_add = self.lipid_attributes[attr].get(node_name)
                            if to_add is None and attr not in STATIC_NODE_PROPERTIES:
                                if node_name in self.data.index:
                                    # in this case the attribute should have been computed
                                    raise ValueError(
                                        f"Something went wrong while computing {attr}. "
                                        f"{node} is present in input data frame, but not in attribute values"
                                    )
                                else:
                                    # this means the node was added during network generation
                                    # and does not have any associated values
                                    # TODO: adapt this behaviour when parsing is all set up!
                                    to_add = np.nan
                            if hasattr(to_add, "item"):
                                # json.serialize cannot handle numpy data types
                                to_add = to_add.item()
                            self.network.nodes[node][attr_] = to_add
                    else:
                        nx.set_edge_attributes(self.network,
                                               len(self.network.edges) * [""],
                                               name=attr_)
                        for edge in self.network.edges:
                            if attr not in STATIC_EDGE_PROPERTIES:
                                edge_name = (self.reverse_mapping.get(edge[0]),
                                             self.reverse_mapping.get(edge[1]))
                            else:
                                edge_name = edge
                            if from_group:
                                to_add = self.interaction_attributes[attr][group].get(edge_name[0], edge_name[1])
                            else:
                                to_add = self.interaction_attributes[attr].get(edge_name[0], edge_name[1])
                            if to_add is None and attr not in STATIC_EDGE_PROPERTIES:
                                # TODO: adapt when parsing is all set up!
                                if edge_name[0] in self.data.index and edge_name[1] in self.data.index:
                                    raise ValueError(
                                        f"Something went wrong while computing {attr}. "
                                        f"{edge[0]} and {edge[1]} are present in input data frame, but not in attribute values"
                                    )
                                else:
                                    to_add = np.nan
                            if hasattr(to_add, "item"):
                                # json.serialize cannot handle numpy data types
                                to_add = to_add.item()
                            self.network.edges[edge][attr_] = to_add
            else:
                if nodes:
                    for node in self.network.nodes:
                        node_name = node if attr in STATIC_NODE_PROPERTIES else self.reverse_mapping.get(node)
                        to_add = self.lipid_attributes[attr].get(node_name)
                        if to_add is None and attr not in STATIC_NODE_PROPERTIES:
                            if node_name in self.data.index:
                                # in this case the attribute should have been computed
                                raise ValueError(
                                    f"Something went wrong while computing {attr}. "
                                    f"{node} is present in input data frame, but not in attribute values"
                                )
                            else:
                                # this means the node was added during network generation
                                # and does not have any associated values
                                # TODO: adapt this behaviour when parsing is all set up!
                                to_add = np.nan
                        if hasattr(to_add, "item"):
                            # json.serialize cannot handle numpy data types
                            to_add = to_add.item()
                        self.network.nodes[node][attr] = to_add
                else:
                    for edge in self.network.edges:
                        if attr not in STATIC_EDGE_PROPERTIES:
                            edge_name = (self.reverse_mapping.get(edge[0]),
                                         self.reverse_mapping.get(edge[1]))
                        else:
                            edge_name = edge
                        to_add = self.interaction_attributes[attr].get(edge[0], edge[1])
                        if to_add is None and attr not in STATIC_EDGE_PROPERTIES:
                            # TODO: adapt when parsing is all set up!
                            if edge_name[0] in self.data.index and edge_name[1] in self.data.index:
                                raise ValueError(
                                    f"Something went wrong while computing {attr}. "
                                    f"{edge[0]} and {edge[1]} are present in input data frame, but not in attribute values"
                                )
                            else:
                                to_add = np.nan
                        if hasattr(to_add, "item"):
                            # json.serialize cannot handle numpy data types
                            to_add = to_add.item()
                        self.network.edges[edge][attr] = to_add
        else:
            if nodes:
                for node in self.network.nodes:
                    node_name = node if attr in STATIC_NODE_PROPERTIES else self.reverse_mapping.get(node)
                    to_add = self.lipid_attributes[attr].get(node_name)
                    if to_add is None and attr not in STATIC_NODE_PROPERTIES:
                        if node_name in self.data.index:
                            # in this case the attribute should have been computed
                            raise ValueError(
                                f"Something went wrong while computing {attr}. "
                                f"{node} is present in input data frame, but not in attribute values"
                            )
                        else:
                            # this means the node was added during network generation
                            # and does not have any associated values
                            # TODO: adapt this behaviour when parsing is all set up!
                            to_add = np.nan
                    if hasattr(to_add, "item"):
                        # json.serialize cannot handle numpy data types
                        to_add = to_add.item()
                    self.network.nodes[node][attr] = to_add
            else:
                for edge in self.network.edges:
                    if attr not in STATIC_EDGE_PROPERTIES:
                        edge_name = (self.reverse_mapping.get(edge[0]),
                                     self.reverse_mapping.get(edge[1]))
                    else:
                        edge_name = edge
                    to_add = self.interaction_attributes[attr].get(edge[0], edge[1])
                    if to_add is None and attr not in STATIC_EDGE_PROPERTIES:
                        # TODO: adapt when parsing is all set up!
                        if edge_name[0] in self.data.index and edge_name[1] in self.data.index:
                            raise ValueError(
                                f"Something went wrong while computing {attr}. "
                                f"{edge[0]} and {edge[1]} are present in input data frame, but not in attribute values"
                            )
                        else:
                            to_add = np.nan
                    if hasattr(to_add, "item"):
                        # json.serialize cannot handle numpy data types
                        to_add = to_add.item()
                    if attr == "enzyme_id" and not self.directed:
                        to_add += f"<br>{self.network.edges[(edge[1], edge[0])][attr]}"
                    self.network.edges[edge][attr] = to_add

    @staticmethod
    def _set_min_max_scale_(
        values: np.ndarray,
        vmax: float = None,
        min_to_zero: bool = True
    ) -> Tuple[float, float]:
        min_ = values.min()
        if min_ < 0:
            if vmax is None:
                max_ = max(abs(values.min()),
                           abs(values.max()))
            else:
                max_ = vmax
            min_ = -max_
        else:
            if min_to_zero:
                min_ = 0
            if vmax is None:
                max_ = values.max()
            else:
                max_ = vmax
        return min_, max_

    def _generate_edge_colours_(
        self, attr: str,
        discrete: bool = True, cmap: str = "tab10",
        group: Union[str, tuple] = None,
        vmin: float = None, vmax: float = None,
        colours_to_hex: bool = False,
        group_attr: str = None
    ) -> Tuple[dict, list]:
        if attr == "correlation_changes" or attr == "partial_correlation_changes":
            if colours_to_hex:
                edge_colour_map = {
                    "significant to unsignificant": to_hex("tab:cyan"),
                    "unsignificant to significant": to_hex("tab:green"),
                    "unchanged significant": to_hex("tab:red"),
                    "unsignificant": "#e1e5e7",
                    "positive to negative": to_hex("tab:blue"),
                    "negative to positive": to_hex("tab:orange"),
                    None: to_hex("black")
                }
            else:
                edge_colour_map = {
                    "significant to unsignificant": "tab:cyan",
                    "unsignificant to significant": "tab:green",
                    "unchanged significant": "tab:red",
                    "unsignificant": "#e1e5e7",
                    "positive to negative": "tab:blue",
                    "negative to positive": "tab:orange",
                    None: to_hex("black")
                }
            edge_colours = [
                edge_colour_map[self.interaction_attributes[attr][group].get(self.reverse_mapping.get(edge[0]),
                                                                             self.reverse_mapping.get(edge[1]))]
                for edge in self.network.edges
            ]
            return edge_colour_map, edge_colours
        if self._attr_group_size_[attr] == 0:
            group = None
        if discrete:
            if group is None:
                attr_set = self.interaction_attributes[attr]
                if isinstance(attr_set, dict):
                    keys = attr_set.keys()
                    if len(keys) == 1:
                        attr_set = attr_set[list(keys)[0]]
                    else:
                        raise ValueError(
                            f"Multiple group options found for {attr}."
                            " Please specify which should be used by using the 'groups' parameter"
                        )
                attr_val_set = unique_elements(attr_set)
            else:
                attr_val_set = unique_elements(self.interaction_attributes[attr][group])
            if attr_val_set.size > 10 and cmap == "tab10":
                cmap = "tab20"
            if attr_val_set.size > 20:
                custom_map = _generate_colormap_(attr_val_set.size)
                colours = [custom_map(i) for i in range(attr_val_set.size)]
            else:
                colours = [plt.get_cmap(cmap)(i)
                           for i in range(attr_val_set.size)]
            edge_colour_map = dict(zip(attr_val_set, colours))
            if group_attr is not None:
                attr = group_attr
            if colours_to_hex:
                edge_colours = [to_hex(edge_colour_map.get(self.network.edges[edge][attr], (0.84, 0.84, 0.84)))
                                for edge in self.network.edges]
            else:
                edge_colours = [edge_colour_map.get(self.network.edges[edge][attr], (0.84, 0.84, 0.84))
                                for edge in self.network.edges]
        else:
            if cmap == "tab10":
                # NOTE: seismic is bad here because 0 values will be non-visible
                cmap = "coolwarm"
            if group is None:
                vals = self.interaction_attributes[attr]
                if isinstance(vals, dict):
                    keys = vals.keys()
                    if len(keys) == 1:
                        vals = vals[list(keys)[0]]
                    else:
                        raise ValueError(
                            f"Multiple group options found for {attr}."
                            " Please specify which should be used by using the 'groups' parameter"
                        )
            else:
                vals = self.interaction_attributes[attr][group]
            val_arr = vals.data
            if np.isnan(val_arr).all():
                vals = 5

            min_, max_ = self._set_min_max_scale_(val_arr, vmax)
            if np.isnan(min_):
                min_ = val_arr[~np.isnan(val_arr)].min()
                if np.isnan(min_):
                    min_ = 0
            if np.isnan(max_) or min_ == max_:
                max_ = val_arr[~np.isnan(val_arr)].max()
                if np.isnan(max_):
                    max_ = min_ + 1

            scm = ScalarMappable(
                norm=Normalize(
                    vmin=min_,
                    vmax=max_
                ),
                cmap=cmap
            )
            if colours_to_hex:
                edge_colours = [to_hex(scm.to_rgba(vals.get(self.reverse_mapping.get(edge[0]),
                                                            self.reverse_mapping.get(edge[1]),
                                                            np.nan)))
                                for edge in self.network.edges]
            else:
                edge_colours = [scm.to_rgba(vals.get(self.reverse_mapping.get(edge[0]),
                                                     self.reverse_mapping.get(edge[1]),
                                                     np.nan))
                                for edge in self.network.edges]
            edge_colour_map = {"min": -max_,
                               "max": max_,
                               "cmap": cmap}

        self.edge_colours[attr] = (edge_colour_map, edge_colours)
        return edge_colour_map, edge_colours

    def _generate_node_colours(
        self, attr: str,
        discrete: bool = True, cmap: str = "tab10",
        group: Union[str, tuple] = None,
        vmin: float = None, vmax: float = None,
        colours_to_hex: bool = False,
        group_attr: str = None
    ) -> Tuple[dict, list]:
        if attr == "lipid_class":
            if colours_to_hex:
                # TODO: test mapping of unknown lipid colours
                node_colours = [
                    LIPID_CLASS_COLOURS.get(self.network.nodes[node]["lipid_class"], "#000000")
                    for node in self.network.nodes
                ]
                # NOTE: this is necessary to also include lipid classes not covered by our default
                # colour scheme
                node_colour_map = {
                    lipid_class: LIPID_CLASS_COLOURS.get(lipid_class, "#000000")
                    for lipid_class in np.unique(list(self.lipid_attributes["lipid_class"].values()))
                }
            else:
                node_colours = [
                    to_rgba(LIPID_CLASS_COLOURS.get(self.network.nodes[node]["lipid_class"], "black"))
                    for node in self.network.nodes
                ]
                # NOTE: this is necessary to also include lipid classes not covered by our default
                # colour scheme
                node_colour_map = {
                    lipid_class: to_rgba(LIPID_CLASS_COLOURS.get(lipid_class, "black"))
                    for lipid_class in np.unique(list(self.lipid_attributes["lipid_class"].values()))
                }
        else:
            if self._attr_group_size_[attr] == 0:
                group = None
            if discrete:
                if group is None:
                    attr_val_set = unique_elements(self.lipid_attributes[attr])
                else:
                    attr_val_set = unique_elements(self.lipid_attributes[attr][group])
                if attr_val_set.size > 10 and cmap == "tab10":
                    cmap = "tab20"
                if attr_val_set.size > 20:
                    colours = _generate_colormap_(attr_val_set.size)
                else:
                    colours = [plt.get_cmap(cmap)(i)
                               for i in range(attr_val_set.size)]
                node_colour_map = dict(zip(attr_val_set, colours))
                if group_attr is not None:
                    attr = group_attr
                if colours_to_hex:
                    node_colours = [to_hex(node_colour_map[self.network.nodes[node][attr]])
                                    for node in self.network.nodes]
                else:
                    node_colours = [node_colour_map[self.network.nodes[node][attr]]
                                    for node in self.network.nodes]
            else:
                if cmap == "tab10":
                    cmap = "seismic"
                if group is None:
                    try:
                        vals = self.lipid_attributes[attr]
                    except KeyError:
                        raise KeyError(
                            f'{attr} has not been computed yet!'
                        )
                else:
                    try:
                        vals = self.lipid_attributes[attr][group]
                    except KeyError:
                        raise KeyError(
                            f'{attr} has not been computed for group {group} yet!'
                        )

                val_arr = np.array(list(vals.values()))

                index_attr = attr not in ["c_index", "db_index", "chain_length", "desaturation",
                                          "oh_index", "hydroxylation"]
                min_, max_ = self._set_min_max_scale_(val_arr, vmax,
                                                      min_to_zero=index_attr)
                if np.isnan(min_):
                    min_ = np.min(val_arr[~np.isnan(val_arr)])
                    if np.isnan(min_):
                        min_ = 0
                if np.isnan(max_) or min_ == max_:
                    max_ = np.max(val_arr[~np.isnan(val_arr)])
                    if np.isnan(max_):
                        max_ = min_ + 1
                if vmin is not None:
                    min_ = vmin
                scm = ScalarMappable(
                    norm=Normalize(
                        vmin=min_,
                        vmax=max_
                    ),
                    cmap=cmap
                )
                if colours_to_hex:
                    node_colours = [to_hex(scm.to_rgba(vals.get(self.reverse_mapping.get(node), np.nan)))
                                    for node in self.network.nodes]
                else:
                    node_colours = [scm.to_rgba(vals.get(self.reverse_mapping.get(node), np.nan))
                                    for node in self.network.nodes]
                if np.isnan(val_arr).any():
                    node_colour_map = {"min": min_,
                                       "max": max_,
                                       "nan": np.nan,
                                       "cmap": cmap}
                else:
                    node_colour_map = {"min": min_,
                                       "max": max_,
                                       "cmap": cmap}

        self.node_colours[attr] = (node_colour_map, node_colours)
        return node_colour_map, node_colours

    def _discrete_legend_(
        self, attr: str,
        nodes: bool = True, **kwargs
    ) -> List[Line2D]:
        if nodes:
            # node labels => scatters
            legend_map = self.node_colours[attr][0]
            markersize = kwargs.pop("markersize", 12)
            handles = [Line2D([0], [0], color="w", marker="o",
                              markerfacecolor=col, label=group,
                              markersize=markersize,
                              **kwargs)
                       for group, col in legend_map.items()]
        else:
            # edge labels => thick lines
            legend_map = self.edge_colours[attr][0]
            lw = kwargs.pop("lw", 4)
            handles = [Line2D([0], [0], color=col,
                              lw=lw, label=group,
                              **kwargs)
                       for group, col in legend_map.items()]

        return handles

    def _continuous_legend_(
        self, attr: str,
        ax: plt.axis = None,
        nodes: bool = True, **kwargs
    ) -> Colorbar:
        if nodes:
            legend_map = self.node_colours[attr][0]
        else:
            legend_map = self.edge_colours[attr][0]
        scm = ScalarMappable(norm=Normalize(vmin=legend_map["min"],
                                            vmax=legend_map["max"]),
                             cmap=legend_map["cmap"])
        return plt.colorbar(scm, ax=ax, **kwargs)

    @staticmethod
    def _scale_dict_(
        sizes: Dict[str, float],
        scale: Tuple[float, float],
        abs_: bool = False,
        map_as_ex: bool = False,
        vmax: float = None,
        map_data_names: dict = None
    ) -> Tuple[Dict[str, float], Dict[float, float]]:
        scale_sizes = np.array(list(sizes.values()))
        if np.isnan(scale_sizes).all():
            # arbitraty default
            scale_sizes = np.zeros(scale_sizes.shape) + 5
        # if abs_:
        #     scale_sizes = abs(scale_sizes)  # NOTE: in this case min = 0
        # else:
        nans = np.isnan(scale_sizes)
        if vmax is None:
            max_ = scale_sizes[~nans].max()
        else:
            max_ = vmax
        if abs_:
            min_ = 0
            scale_sizes = abs(scale_sizes)
        else:
            min_ = scale_sizes[~nans].min()
            scale_sizes = scale_sizes - min_
        if max_ - min_ != 0:
            scale_sizes = scale_sizes / (max_ - min_)
        if abs_:
            scale_sizes = abs(scale_sizes * (scale[1] - scale[0]) + scale[0])
        else:
            scale_sizes = scale_sizes * (scale[1] - scale[0]) + scale[0]
        if map_data_names:
            expanded_scaled = []
            lipid_names = []
            for idx, lipid in enumerate(sizes.keys()):
                for mapping in map_data_names.get(lipid, []):
                    expanded_scaled.append(scale_sizes[idx])
                    lipid_names.append(mapping)
            scaled_sizes = dict(zip(lipid_names, expanded_scaled))
        else:
            scaled_sizes = dict(zip(sizes.keys(),
                                    list(scale_sizes)))
        final_min = scale_sizes[~nans].min()
        final_max = scale_sizes[~nans].max()
        if map_as_ex:
            if nans.any():
                scale_map = {
                    "min": (min_, final_min),
                    "max": (max_, final_max),
                    # arbitrary values to draw nans in legend
                    "nan": (1, 1)
                }
            else:
                scale_map = {
                    "min": (min_, final_min),
                    "max": (max_, final_max)
                }
        else:
            scale_sizes[nans] = final_min / 2
            scale_map = dict(zip(sizes.values(), scale_sizes))
        return scaled_sizes, scale_map

    def _edge_colour_subset_(
        self, attr: str,
        discrete: bool = True, cmap: str = "tab10",
        group: Union[str, tuple] = None,
        vmin: float = None, vmax: float = None
    ) -> Tuple[dict, list]:
        if group is None:
            return self._generate_edge_colours_(
                attr,
                discrete, cmap,
                vmin=vmin, vmax=vmax
            )
        elif len(group) == 1:
            return self._generate_edge_colours_(
                attr,
                discrete, cmap,
                group[0], vmax=vmax,
                vmin=vmin
            )
        else:
            return self._generate_edge_colours_(
                attr,
                discrete, cmap,
                group, vmax=vmax,
                vmin=vmin
            )

    def _node_colour_subset_(
        self, attr: str,
        discrete: bool = True, cmap: str = "tab10",
        group: Union[str, tuple] = None,
        vmin: float = None, vmax: float = None
    ) -> Tuple[dict, list]:
        if group is None:
            return self._generate_node_colours(
                attr,
                discrete, cmap,
                vmax=vmax, vmin=vmin)
        elif len(group) == 1:
            return self._generate_node_colours(
                attr,
                discrete, cmap,
                group[0], vmax=vmax,
                vmin=vmin
            )
        else:
            return self._generate_node_colours(
                attr,
                discrete, cmap,
                group, vmax=vmax,
                vmin=vmin
            )

    def plot_static_network(
        self,
        layout: Union[Callable, dict] = nx_layout.fruchterman_reingold_layout,
        overwrite_layout: bool = False,
        as_undirected: bool = True,
        edge_colour_attr: str = None,
        overwrite_edge_attr: bool = True,
        edge_map: str = "tab10",
        edge_legend: bool = True,
        edge_size_func: Union[Callable, int] = None,
        edge_size_scale: Tuple[int, int] = (.2, .3),
        edge_size_legend: bool = True,
        edge_size_title: str = "Edge size",
        node_colour_attr: str = None,
        overwrite_node_attr: bool = True,
        node_map: str = "tab10",
        node_legend: bool = True,
        node_size_func: Union[Callable, int] = None,
        node_size_scale: Tuple[int, int] = (50, 400),
        node_size_legend: bool = True,
        node_size_title: str = "Node size",
        edge_group_subset: Union[tuple, list, set] = None,
        node_group_subset: Union[tuple, list, set] = None,
        vmin: float = None,
        vmax: float = None,
        ax: plt.axis = None,
        figargs: dict = None,
        layout_args: dict = None,
        show: bool = False,
        **kwargs
    ) -> plt.axis:
        """
        Plotting the computed network in a static manner using networkx and matplotlib

        Parameters
        ----------
        :param layout: networkx.layout function or dict, optional, default nx_layout.fruchterman_reingold_layout
            If a dict specifying node position this is used to
            plot the network. If a callable it is used to
            compute the layout.
            If self.layout is None or overwrite_layout is True
            it will be stored in self.layout

        :param overwrite_layout: bool, optional, default False
            Whether to overwrite self.layout

        :param as_undirected: bool, optional, default True
            This parameter currently has no effect!
            Whether to show the network as directed or undirected.
            If directed, lipid class reactions will not be symmetric,
            i.e. PC -> PE could be possible but not PE -> PC.

        :param edge_colour_attr: str, optional
            Attribute to use for edge colours.
            Available options: correlations, partial_correlations,
            reaction_type, correlation_changes, partial_correlation_changes.
            All metrics except reaction_type have to be computed beforehand.

        :param overwrite_edge_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.interaction_attributes

        :param edge_map: str, optional, default 'tab10'
            Colourmap to use for edge colouring. Default for continuous
            attributes is 'viridis'

        :param edge_legend: bool, optional, default True
            Whether to show a legend for edge colours

        :param edge_size_func: Callable or int, optional
            Used to compute edge sizes if a function.
            Else set as constant edge size.

        :param edge_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted edge sizes. The actual values will be scaled
            to fit this range.

        :param edge_size_legend: bool, optional, True
            Whether to show the legend for edge sizes

        :param edge_size_title: str, optional, default 'Edge size'
            Title of the edge size legend

        :param node_colour_attr: str, optional
            Specifies the attribute to use for determining node colours.
            Available options are: fold_changes, pvalues, nlog_pvalues,
            lipid_class, c_index, db_index

        :param overwrite_node_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.lipid_attributes

        :param node_map: str, optional, default 'tab10'
            Colourmap to use for node colouring. Default for continuous
            attributes is 'viridis'

        :param node_legend: bool, optional, default True
            Whether to show node colour legend

        :param node_size_func: Callable or int, optional
            Used to compute node sizes if a function.
            Else set as constant node size.

        :param node_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted node sizes. The actual values will be scaled
            to fit this range.

        :param node_size_legend: bool, optional, default True
            Whether to show the legend for node sizes

        :param node_size_title: str, optional, default 'Node size'
            Title of node size legend

        :param edge_group_subset: tuple or list of size 2, optional
            Group-comparison to show in edge colouring/sizing

        :param node_group_subset: tuple or list of size 2, optional
            Group-comparison to show in node colouring/sizing

        :param vmin: float, optional
            Minimum value of the legend (for continuous scales).
            If not given it will be set to 0 (for only positive
            arrays) or to -max(abs(min), abs(max)) (for zero-centred
            colours).
            Setting vmin can lead to un-centred colour scales!

        :param vmax: float, optional
            Maximum value of the legend (for continuous scales).
            If vmin is not specified, the minimum value will be
            either 0 (if all values are positive) or -vmax

        :param ax: plt.axis, optional
            matplotlib axis to plot onto

        :param figargs: dict, optional
            keyword arguments to pass to plt.figure.
            Only relevant if ax=None (default)

        :param layout_args: dict, optional
            keyword arguments to pass to layout.
            Only relevant if layout is not a function (default)

        :param show : bool, optional, default False
            Whether to show the plot

        :param kwargs:
            keyword arguments to pass to networkx.draw


        Returns
        -------
        :return plt.axis on which the network is plotted


        Raises
        ------
        NotComputedError
            If edge_colour_attr or node_colour_attr have not been
            computed before

        ValueError
            If edge_colour_attr or node_colour_attr are not in the
            list of available options
        """
        edge_discrete = None
        node_discrete = None
        if edge_colour_attr is not None:
            self._check_attributes_(
                edge_colour_attr,
                node_colour_attr
            )
            # check if attributes have been added to network
            # edge attribute
            self._add_network_attribute_(
                edge_colour_attr, nodes=False,
                group_subset=edge_group_subset,
                overwrite=overwrite_edge_attr
            )
            edge_discrete = self._discrete_map_[edge_colour_attr]
            edge_colours = self._edge_colour_subset_(edge_colour_attr,
                                                     edge_discrete,
                                                     edge_map,
                                                     group=edge_group_subset)
        else:
            edge_legend = False
            edge_colours = ["tab:gray" for _ in range(len(self.network.edges))]
        # node attribute
        if node_colour_attr is not None:
            self._add_network_attribute_(
                node_colour_attr, nodes=True,
                group_subset=node_group_subset,
                overwrite=overwrite_node_attr
            )
            node_discrete = self._discrete_map_[node_colour_attr]
            node_colours = self._node_colour_subset_(node_colour_attr,
                                                     node_discrete,
                                                     node_map,
                                                     node_group_subset,
                                                     vmin=vmin, vmax=vmax)
        else:
            node_legend = False
            node_colours = ["tab:blue" for _ in range(len(self.network.nodes))]

        # node sizes:
        # ===========
        node_size_legend_ = False
        node_sizes = None
        if kwargs.get("node_size") is not None:
            node_size = kwargs.pop("node_size")
            if isinstance(node_size, int) or isinstance(node_size, float):
                node_size = {node: node_size for node in self.network.nodes}
            elif isinstance(node_size, list) or isinstance(node_size, set):
                node_size = dict(zip(self.network.nodes, node_size))
        else:
            if node_size_func is None:
                sizes = nx.betweenness_centrality(self.network)
                scale_sizes = _range_scale_(x=np.array(list(sizes.values())),
                                            a=node_size_scale[0],
                                            b=node_size_scale[1])
                node_size = dict(zip(sizes.keys(),
                                     list(scale_sizes)))
                node_size_legend_ = True
                node_sizes = (min(list(sizes.values())),
                              max(list(sizes.values())))
            elif isinstance(node_size_func, int):
                node_size = dict(zip(self.network.nodes,
                                     len(self.network.nodes) * [node_size_func]))
            elif isinstance(node_size_func, Callable):
                node_size = node_size_func(self.network)
                node_size_legend_ = True
            else:
                node_size = dict(zip(self.network.nodes,
                                     len(self.network.nodes) * [23]))

        # edge sizes:
        # ===========
        edge_sizes = None
        if kwargs.get("width") is not None:
            edge_size = kwargs.pop("width")
            edge_size_legend_ = False
        else:
            edge_size_legend_ = False
            if edge_size_func is None:
                sizes = nx.edge_betweenness_centrality(self.network)
                scale_sizes = _range_scale_(x=np.array(list(sizes.values())),
                                            a=edge_size_scale[0],
                                            b=edge_size_scale[1])
                edge_size = dict(zip(sizes.keys(),
                                     list(scale_sizes)))
                edge_size_legend_ = True
                edge_sizes = (min(list(sizes.values())),
                              max(list(sizes.values())))
            elif isinstance(edge_size_func, int):
                edge_size = dict(zip(self.network.edges,
                                     len(self.network.edges) * [edge_size_func]))
            elif isinstance(edge_size_func, Callable):
                edge_size = edge_size_func(self.network)
                if not isinstance(edge_size, dict):
                    edge_size = dict(zip(self.network.edges,
                                         edge_size))
                edge_size_legend_ = True
            else:
                edge_size = dict(zip(self.network.edges,
                                     len(self.network.edges) * [5]))

        if ax is None:
            if figargs is None:
                fig, ax = plt.subplots()
            else:
                fig, ax = plt.subplots(**figargs)
            ax.set_xticks([])
            ax.set_yticks([])

        pre_layout = hasattr(self, "layout")
        if not pre_layout:
            if layout_args is None:
                self.layout = layout(self.network)
            else:
                self.layout = layout(self.network, **layout_args)
        elif overwrite_layout or self.layout is None:
            if layout_args is None:
                self.layout = layout(self.network)
            else:
                self.layout = layout(self.network, **layout_args)

        if as_undirected:
            # NOTE: this has no influence here!
            if isinstance(self.network, nx.DiGraph):
                nx.draw(self.network.to_undirected(),
                        node_color=node_colours[1],
                        edge_color=edge_colours[1],
                        ax=ax,
                        node_size=[node_size[node] for node in self.network.nodes],
                        width=[edge_size[edge] for edge in self.network.edges],
                        pos=self.layout,
                        **kwargs)
            else:
                nx.draw(self.network,
                        node_color=node_colours[1],
                        edge_color=edge_colours[1],
                        ax=ax,
                        node_size=[node_size[node] for node in self.network.nodes],
                        width=[edge_size[edge] for edge in self.network.edges],
                        pos=self.layout,
                        **kwargs)
        else:
            nx.draw(self.network,
                    node_color=node_colours[1],
                    edge_color=edge_colours[1],
                    ax=ax,
                    node_size=[node_size[node] for node in self.network.nodes],
                    width=[edge_size[edge] for edge in self.network.edges],
                    pos=self.layout,
                    **kwargs)
        # colour legends
        # ==============
        if node_legend:
            if node_discrete:
                hands = self._discrete_legend_(node_colour_attr,
                                               nodes=True)
                if edge_discrete:
                    plt.gca().add_artist(
                        plt.legend(handles=hands,
                                   title=node_colour_attr,
                                   loc=1,
                                   bbox_to_anchor=(1.2, 1))
                    )
                else:
                    plt.gca().add_artist(
                        plt.legend(handles=hands,
                                   title=node_colour_attr,
                                   loc=1,
                                   bbox_to_anchor=(1.35, 1))
                    )
            else:
                nbar = self._continuous_legend_(node_colour_attr,
                                                ax, nodes=True)
                nbar.ax.set_title(node_colour_attr)
        if edge_legend:
            if edge_discrete:
                hands = self._discrete_legend_(edge_colour_attr,
                                               nodes=False)
                plt.gca().add_artist(
                    plt.legend(handles=hands,
                               title=edge_colour_attr,
                               loc=1,
                               bbox_to_anchor=(1.35, 1))
                )
            else:
                ebar = self._continuous_legend_(edge_colour_attr,
                                                ax, nodes=False)
                ebar.ax.set_title(edge_colour_attr)
        # size legends
        # ==============
        # TODO: choose node/edge size in a way such that the legend
        #       can represent the actual property
        if node_size_legend and node_size_legend_:
            if node_sizes is None:
                node_sizes = (min(list(node_size.values())),
                              max(list(node_size.values())))
                node_size_scale = None
            plt.gca().add_artist(
                plt.legend(handles=_size_legend_(node_sizes,
                                                 node_size_scale,
                                                 nodes=True),
                           loc="upper left", bbox_to_anchor=(-.15, 1),
                           title=node_size_title)
            )
        if edge_size_legend and edge_size_legend_:
            if edge_sizes is None:
                edge_sizes = (min(list(edge_size.values())),
                              max(list(edge_size.values())))
                edge_size_scale = None
            plt.gca().add_artist(
                plt.legend(handles=_size_legend_(edge_sizes,
                                                 edge_size_scale,
                                                 nodes=False),
                           loc="upper left", bbox_to_anchor=(-.15, .7),
                           title=edge_size_title)
            )

        plt.tight_layout()
        if show:
            plt.show()
        return ax

    def network_to_pyvis(
        self,
        edge_colour_attr: str = None,
        overwrite_edge_attr: bool = True,
        edge_cmap: str = "tab10",
        edge_size_func: Union[Callable, int] = None,
        edge_size_scale: Tuple[int, int] = (.2, .3),
        node_colour_attr: str = None,
        overwrite_node_attr: bool = True,
        node_cmap: str = "tab10",
        node_size_func: Union[Callable, int] = None,
        node_size_scale: Tuple[int, int] = (50, 400),
        edge_group_subset: Union[tuple, list, set] = None,
        node_group_subset: Union[tuple, list, set] = None,
        net: VisParser = None,
        as_directed: bool = False,
        vmin: float = None,
        vmax: float = None,
        **kwargs
    ) -> VisParser:
        """
        Converting the generated network from networkx format to pyvis format

        Parameters
        ----------
        :param edge_colour_attr: str, optional
            Attribute to use for edge colours.
            Available options: correlations, partial_correlations,
            reaction_type, correlation_changes, partial_correlation_changes.
            All metrics except reaction_type have to be computed beforehand.

        :param overwrite_edge_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.interaction_attributes

        :param edge_cmap: str, optional, default 'tab10'
            Colourmap to use for edge colouring. Default for continuous
            attributes is 'viridis'

        :param edge_size_func: Callable or int, optional
            Used to compute edge sizes if a function.
            Else set as constant edge size.

        :param edge_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted edge sizes. The actual values will be scaled
            to fit this range.

        :param node_colour_attr: str, optional
            Specifies the attribute to use for determining node colours.
            Available options are: fold_changes, pvalues, nlog_pvalues,
            lipid_class, c_index, db_index

        :param overwrite_node_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.lipid_attributes

        :param node_size_func: Callable or int, optional
            Used to compute node sizes if a function.
            Else set as constant node size.

        :param node_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted node sizes. The actual values will be scaled
            to fit this range.

        :param node_cmap: str, optional, default 'tab10'
            Colourmap to use for edge colouring. Default for continuous
            attributes is 'viridis'

        :param edge_group_subset: tuple or list of size 2, optional
            Group-comparison to show in edge colouring/sizing

        :param node_group_subset: tuple or list of size 2, optional
            Group-comparison to show in node colouring/sizing

        :param net: pyvis.network.Network, optional
            If given this instance will be used instead of generating
            a new one within the function

        :param as_directed: bool, optional, default False
            This has currenlty no effect!
            Whether to show a direted graph

        :param vmin: float, optional
                Minimum value of the legend (for continuous scales).
                If not given it will be set to 0 (for only positive
                arrays) or to -max(abs(min), abs(max)) (for zero-centred
                colours).
                Setting vmin can lead to un-centred colour scales!

        :param vmax : float, optional
            Maximum value of the legend (for continuous scales).
            If vmin is not specified, the minimum value will be
            either 0 (if all values are positive) or -vmax


        :param kwargs:
            keyword arguments to pass to pyvis.network.Network. Only
            releveant if net=None (default)

        Returns
        -------
        :return linex2.vis_utils.VisParser
        """
        self._check_attributes_(
            edge_colour_attr, node_colour_attr
        )
        # check if attributes have been added to network
        # edge attribute
        self._add_network_attribute_(
            edge_colour_attr, nodes=False,
            group_subset=edge_group_subset,
            overwrite=overwrite_edge_attr
        )
        edge_discrete = self._discrete_map_[edge_colour_attr]
        # node attribute
        self._add_network_attribute_(
            node_colour_attr, nodes=True,
            group_subset=node_group_subset,
            overwrite=overwrite_node_attr
        )
        node_discrete = self._discrete_map_[node_colour_attr]

        # generate colours
        edge_colours = self._edge_colour_subset_(edge_colour_attr,
                                                 edge_discrete,
                                                 edge_cmap,
                                                 edge_group_subset)
        node_colours = self._node_colour_subset_(node_colour_attr,
                                                 node_discrete,
                                                 node_cmap,
                                                 node_group_subset,
                                                 vmin=vmin, vmax=vmax)

        int_net = self.network.copy()
        if node_size_func is None:
            sizes = nx.betweenness_centrality(int_net)
            scale_sizes = _range_scale_(x=np.array(list(sizes.values())),
                                        a=node_size_scale[0],
                                        b=node_size_scale[1])
            node_size = dict(zip(sizes.keys(),
                                 list(scale_sizes)))
        elif isinstance(node_size_func, int):
            node_size = dict(zip(int_net.nodes,
                                 len(int_net.nodes) * [node_size_func]))
        elif isinstance(node_size_func, Callable):
            node_size = node_size_func(int_net)
        elif isinstance(node_size_func, dict):
            node_size = node_size_func
        else:
            node_size = dict(zip(int_net.nodes,
                                 len(int_net.nodes) * [5]))
        for i, node in enumerate(int_net.nodes):
            int_net.nodes[node]["value"] = node_size[node]
            int_net.nodes[node]["color"] = to_hex(node_colours[1][i])
            node_title = f"<strong>{node}</strong>:"
            prime = "<br><br><strong>{0}</strong>:<br>{1}"
            for prop in ["fold_changes", "pvalues"]:
                if self.lipid_attributes.get(prop) is not None:
                    sup = re.sub("s$", "", prop)
                    group_vals = self.lipid_attributes[prop]
                    # if fold_changes and pvalues are computes groups
                    # must have been specified at some point
                    for group, vals in group_vals.items():
                        node_title += prime.format(sup, f"{group}: {vals[node]}")
            int_net.nodes[node]["title"] = node_title

        if edge_size_func is None:
            sizes = nx.edge_betweenness_centrality(int_net)
            scale_sizes = _range_scale_(x=np.array(list(sizes.values())),
                                        a=edge_size_scale[0],
                                        b=edge_size_scale[1])
            edge_size = dict(zip(sizes.keys(),
                                 list(scale_sizes)))
        elif isinstance(edge_size_func, int):
            edge_size = dict(zip(int_net.edges,
                                 len(int_net.edges) * [edge_size_func]))
        elif isinstance(edge_size_func, Callable):
            edge_size = edge_size_func(int_net)
        elif isinstance(edge_size_func, dict):
            edge_size = edge_size_func
        else:
            edge_size = dict(zip(int_net.edges,
                                 len(int_net.edges) * [5]))

        props_oi = [prop for prop, val in self.interaction_attributes.items()
                    if val is not None]
        if isinstance(edge_group_subset, list):
            if len(edge_group_subset) == 1:
                def get_prop(x):
                    return self.interaction_attributes[x][edge_group_subset[0]]
            else:
                def get_prop(x):
                    return self.interaction_attributes[x][tuple(edge_group_subset)]
        else:
            def get_prop(x):
                return self.interaction_attributes[x]
        for i, edge in enumerate(int_net.edges):
            int_net.edges[edge]["value"] = edge_size[edge]
            int_net.edges[edge]["color"] = to_hex(edge_colours[1][i])
            edge_title = f"<strong>{int_net.edges[edge]['reaction_type']}</strong><br>"
            prime = "<strong>{0}</strong>:<br>{1}<br><br>"
            for prop in props_oi:
                sup = re.sub("s$", "", prop)
                if self._attr_group_size_[prop] == 0:
                    if prop != "enzyme_id":
                        val = self.interaction_attributes[prop].get(edge[0], edge[1], '')
                    else:
                        if as_directed:
                            renz = self.interaction_attributes[prop].get(edge[0], edge[1], '')
                            if isinstance(renz, str):
                                val = f"{renz.split(':')[1]}"
                            else:
                                val = str(renz)
                        else:
                            val_ij = self.interaction_attributes[prop].get(edge[0], edge[1], '')
                            val_ji = self.interaction_attributes[prop].get(edge[1], edge[0], '')
                            val = f"{val_ij}<br>{val_ji}"
                else:
                    try:
                        val = get_prop(prop).loc[edge[0], edge[1]]
                    # FIXME
                    # this is not a nice solution => make sure it's possible to
                    # correctly get edge values when supplying single groups
                    # for nodes
                    except KeyError:
                        val = None
                if val is not None:
                    if isinstance(val, float):
                        edge_title += prime.format(sup, round(val, ndigits=3))
                    else:
                        edge_title += prime.format(sup, val)
            int_net.edges[edge]["title"] = re.sub("<br>$", "", edge_title)

        if net is None:
            net = VisParser(directed=as_directed & isinstance(int_net, nx.DiGraph),
                            **kwargs)
        elif isinstance(net, Network):
            net = VisParser.from_pyvis_network(net, **kwargs)
        net.inherit_edge_colors(False)
        if as_directed and isinstance(int_net, nx.DiGraph):
            net.from_nx(int_net.to_directed())
        else:
            net.from_nx(int_net)
        # TODO: adapt to take continuous colour maps
        #       and node/edge sizes
        net.generate_legend(
            node_colours=node_colours[0],
            edge_colours=edge_colours[0]
        )
        return net

    def plot_interactive_network(
        self,
        file: str = "LipidNetwork.html",
        edge_colour_attr: str = None,
        overwrite_edge_attr: bool = True,
        edge_cmap: str = "tab10",
        edge_size_func: Union[Callable, int] = None,
        edge_size_scale: Tuple[int, int] = (2e-4, 3e-2),
        node_colour_attr: str = None,
        overwrite_node_attr: bool = True,
        node_cmap: str = "tab10",
        node_size_func: Union[Callable, int] = None,
        node_size_scale: Tuple[int, int] = (9, 11),
        edge_group_subset: Union[tuple, list, set] = None,
        node_group_subset: Union[tuple, list, set] = None,
        save: bool = False,
        show: bool = False,
        do_return: bool = False,
        notebook: bool = False,
        net: Network = None,
        show_filters: Union[str, List[str]] = None,
        as_directed: bool = False,
        vmin: float = None, vmax: float = None,
        **kwargs
    ) -> Union[VisParser, None]:
        """
        Plotting the computed network interactively using pyvis/vis.js

        Parameters
        ----------
        :param file: str, optional, default 'LipidNetwork.html'
            Path to which the html file (self-contained) is saved to.

        :param edge_colour_attr: str, optional
            Attribute to use for edge colours.
            Available options: correlations, partial_correlations,
            reaction_type, correlation_changes, partial_correlation_changes.
            All metricx except reaction_type have to be computed beforehand.

        :param overwrite_edge_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.interaction_attributes

        :param edge_cmap: str, optional, default 'tab10'
            Colourmap to use for edge colouring. Default for continuous
            attributes is 'viridis'

        :param edge_size_func: Callable or int, optional
            Used to compute edge sizes if a function.
            Else set as constant edge size.

        :param edge_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted edge sizes. The actual values will be scaled
            to fit this range.

        :param node_colour_attr: str, optional
            Specifies the attribute to use for determining node colours.
            Available options are: fold_changes, pvalues, nlog_pvalues,
            lipid_class, c_index, db_index

        :param overwrite_node_attr: bool, optional, default True
            Whether to overwrite attribute with the given group setting in
            self.lipid_attributes

        :param node_size_func: Callable or int, optional
            Used to compute node sizes if a function.
            Else set as constant node size.

        :param node_size_scale: tuple, optional, default (3, 12)
            Tuple of integers specifying the minimum and maximum
            of plotted node sizes. The actual values will be scaled
            to fit this range.

        :param node_cmap: str, optional, default 'tab10'
            Colourmap to use for edge colouring. Default for continuous
            attributes is 'viridis'

        :param edge_group_subset: tuple or list of size 2, optional
            Group-comparison to show in edge colouring/sizing

        :param node_group_subset: tuple or list of size 2, optional
            Group-comparison to show in node colouring/sizing

        :param save: bool, optional, default False,
            Whether to (only) save the plot

        :param show: bool, optional, default False,
            Whether to open the saved plot in the standard browser

        :param do_return: bool, optional, default False
            Whether to return the pyvis.network.Network object

        :param notebook: bool, optional, default False
            Whether the function is called from within a jupyter
            notebook (required to show interactive plot inline)

        :param net: pyvis.network.Network, optional
            If given this instance will be used instead of generating
            a new one within the function

        :param show_filters: str or list, optional
            Specifies one or multiple filters to activate. See pyvis
            documentation for available filters.

        :param as_directed: bool, optional, default False
            Whether to show a direted graph

        :param vmin: float, optional
            Minimum value of the legend (for continuous scales).
            If not given it will be set to 0 (for only positive
            arrays) or to -max(abs(min), abs(max)) (for zero-centred
            colours).
            Setting vmin can lead to un-centred colour scales!

        :param vmax: float, optional
            Maximum value of the legend (for continuous scales).
            If vmin is not specified, the minimum value will be
            either 0 (if all values are positive) or -vmax

        :param kwargs:
            keyword arguments to pass to pyvis.network.Network. Only
            releveant if net=None (default)

        Returns
        -------
        :return pyvis.network.Network or None
        """
        net = self.network_to_pyvis(
            edge_colour_attr=edge_colour_attr,
            overwrite_edge_attr=overwrite_edge_attr,
            edge_cmap=edge_cmap,
            edge_size_func=edge_size_func,
            edge_size_scale=edge_size_scale,
            node_cmap=node_cmap,
            node_size_func=node_size_func,
            node_colour_attr=node_colour_attr,
            overwrite_node_attr=overwrite_node_attr,
            node_size_scale=node_size_scale,
            edge_group_subset=edge_group_subset,
            node_group_subset=node_group_subset,
            net=net,
            as_directed=as_directed,
            vmin=vmin, vmax=vmax,
            **kwargs
        )
        if as_directed:
            net.set_edge_smooth("straight_cross")
        if show_filters is not None:
            if isinstance(show_filters, str):
                if show_filters == "all":
                    net.show_buttons(filter_=True)
                else:
                    net.show_buttons(filter_=[show_filters])
            else:
                net.show_buttons(filter_=show_filters)
        if do_return:
            return net
        if show:
            net.show(file)
            return
        if save:
            net.write_html(file, notebook)

    def _get_attr_abs_max_(self, attr: str, nodes: bool) -> float:
        attributes = self.lipid_attributes if nodes else self.interaction_attributes
        if attr not in attributes.keys():
            raise KeyError(
                f'{attr} not found in computed attribute list!'
            )
        if not isinstance(attributes[attr], dict):
            raise ValueError(
                f'{attr} have not been computed in a group-specific manner'
            )
        max_ = 0.
        for group, values in attributes[attr].items():
            if isinstance(values, SymmetricMatrix):
                cmax = np.nanmax(abs(values.data))
            elif isinstance(values, dict):
                cmax = np.nanmax(abs(np.array(list(values.values()))))
            else:
                raise ValueError(f'Wrong data type {type(values).__name__}')
            if cmax > max_:
                max_ = cmax
        return max_

    def add_network_colours(
        self, attributes: List[str],
        nodes: bool = True,
        cmaps: Dict[str, str] = None
    ) -> Dict[str, Dict[str, Any]]:
        max_ = None
        if nodes:
            generator = self._generate_node_colours
            setter = nx.set_node_attributes
            keys = self.network.nodes
        else:
            generator = self._generate_edge_colours_
            setter = nx.set_edge_attributes
            keys = self.network.edges
        if cmaps is None:
            cmaps = {"lipid_class": "tab20"}
        to_string = {}
        legends_maps = {}
        for attr in attributes:
            if attr in {'enzyme_gene_name', 'enzyme_uniprot', 'enzyme_id'}:
                continue
            if nodes:
                self._check_attributes_(None, attr)
            else:
                self._check_attributes_(attr, None)
            if self._attr_group_size_[attr] == 0 or \
                not hasattr(self, "unique_groups"):
                self._add_network_attribute_(
                    attr, nodes=nodes, group_subset=None,
                    overwrite=attr not in STATIC_NODE_PROPERTIES and attr not in STATIC_EDGE_PROPERTIES
                )
                if attr in to_string:
                    pass
                attr_colours = generator(
                    attr=attr, discrete=self._discrete_map_[attr],
                    cmap=cmaps.get(attr, "tab10"),
                    colours_to_hex=True
                )
                setter(
                    self.network,
                    dict(zip(keys, attr_colours[1])),
                    name=f"{attr}_colour"
                )
                legends_maps[f"{attr}_colour"] = attr_colours[0]
            elif self._attr_group_size_[attr] == 1:
                if not self._discrete_map_[attr]:
                    max_ = self._get_attr_abs_max_(attr, nodes)
                for group in self.unique_groups:
                    self._add_network_attribute_(
                        attr, nodes=nodes, group_subset=[group],
                        overwrite=attr not in STATIC_NODE_PROPERTIES and attr not in STATIC_EDGE_PROPERTIES,
                        add_group=True
                    )
                    if not self._discrete_map_[attr]:
                        for attr_name, vmax in zip(
                            [f"{attr}_colour_{group}_individual", f"{attr}_colour_{group}_common"],
                            [None, max_]):
                            attr_colours = generator(
                                attr,
                                self._discrete_map_[attr],
                                cmaps.get(attr, "tab10"),
                                group=group,
                                colours_to_hex=True,
                                group_attr=f"{attr}_{group}",
                                vmax=vmax
                            )
                            setter(
                                self.network,
                                dict(zip(keys, attr_colours[1])),
                                name=attr_name
                            )
                            legends_maps[attr_name] = attr_colours[0]
                    else:
                        attr_colours = generator(
                            attr,
                            self._discrete_map_[attr],
                            cmaps.get(attr, "tab10"),
                            group=group,
                            colours_to_hex=True,
                            group_attr=f"{attr}_{group}"
                        )
                        attr_name = f"{attr}_colour_{group}"
                        setter(
                            self.network,
                            dict(zip(keys, attr_colours[1])),
                            name=attr_name
                        )
                        legends_maps[attr_name] = attr_colours[0]
            else:
                if not self._discrete_map_[attr]:
                    max_ = self._get_attr_abs_max_(attr, nodes)
                for comb in self.comparisons:
                    if not self._discrete_map_[attr]:
                        for attr_name, vmax in zip(
                            [f"{attr}_colour_{_tuple_to_string_(comb)}_individual",
                             f"{attr}_colour_{_tuple_to_string_(comb)}_common"],
                            [None, max_]):
                            attr_colours = generator(
                                attr,
                                self._discrete_map_[attr],
                                cmaps.get(attr, "tab10"),
                                group=comb,
                                colours_to_hex=True,
                                group_attr=f"{attr}_{_tuple_to_string_(comb)}",
                                vmax=vmax
                            )
                            setter(
                                self.network,
                                dict(zip(keys, attr_colours[1])),
                                name=attr_name
                            )
                            legends_maps[attr_name] = attr_colours[0]
                    else:
                        self._add_network_attribute_(
                            attr, nodes=nodes, group_subset=comb,
                            overwrite=True, add_group=True,
                        )
                        attr_colours = generator(
                            attr,
                            self._discrete_map_[attr],
                            cmaps.get(attr, "tab10"),
                            group=comb,
                            colours_to_hex=True,
                            group_attr=f"{attr}_{_tuple_to_string_(comb)}"
                        )
                        attr_name = f"{attr}_colour_{_tuple_to_string_(comb)}"
                        setter(
                            self.network,
                            dict(zip(keys, attr_colours[1])),
                            name=attr_name
                        )
                        legends_maps[attr_name] = attr_colours[0]
        return legends_maps

    def add_node_sizes(
        self, attributes: List[str],
        scale: Tuple[float, float]
    ) -> Dict[str, Dict[float, float]]:
        max_ = None
        legends_maps = {}
        abs_ = False
        for attr in attributes:
            if attr in {'enzyme_gene_name', 'enzyme_uniprot', 'enzyme_id'}:
                continue
            if attr == "fold_changes":
                abs_ = False
            if attr in STATIC_NODE_PROPERTIES:
                node_names = self.network.nodes
            else:
                node_names = [self.reverse_mapping.get(node, node)
                              for node in self.network.nodes]
            self._check_attributes_(None, attr)
            if self._attr_group_size_[attr] == 0 or \
                    not hasattr(self, "unique_groups"):
                sizes, na_keys = _get_sizes_report_nas_(self.lipid_attributes[attr],
                                                        node_names)
                attr_size = self._scale_dict_(sizes, scale,
                                              map_as_ex=True)
                if na_keys:
                    for node, val in attr_size[0].items():
                        if np.isnan(val):
                            attr_size[0][node] = scale[0] / 2
                nx.set_node_attributes(
                    self.network, attr_size[0],
                    name=f"{attr}_size"
                )
                legends_maps[f"{attr}_size"] = attr_size[1]
            elif self._attr_group_size_[attr] == 1:
                if not self._discrete_map_[attr]:
                    max_ = self._get_attr_abs_max_(attr, nodes=True)
                for group in self.unique_groups:
                    sizes, na_keys = _get_sizes_report_nas_(self.lipid_attributes[attr][group],
                                                            node_names)
                    if not self._discrete_map_[attr]:
                        for attr_name, vmax in zip(
                                [f"{attr}_size_{group}_individual", f"{attr}_size_{group}_common"],
                                [None, max_]):
                            attr_size = self._scale_dict_(sizes, scale,
                                                          map_as_ex=True,
                                                          vmax=vmax)
                            if na_keys:
                                for node, val in attr_size[0].items():
                                    if np.isnan(val):
                                        attr_size[0][node] = scale[0] / 2
                            nx.set_node_attributes(
                                self.network, attr_size[0],
                                name=attr_name
                            )
                            legends_maps[attr_name] = attr_size[1]
                    else:
                        attr_size = self._scale_dict_(sizes, scale,
                                                      map_as_ex=True)
                        if na_keys:
                            for node, val in attr_size[0].items():
                                if np.isnan(val):
                                    attr_size[0][node] = scale[0] / 2
                        nx.set_node_attributes(
                            self.network, attr_size[0],
                            name=f"{attr}_size_{group}"
                        )
                        legends_maps[f"{attr}_size_{group}"] = attr_size[1]
            else:
                if not self._discrete_map_[attr]:
                    max_ = self._get_attr_abs_max_(attr, nodes=True)
                for comb in self.comparisons:
                    if self.lipid_attributes[attr].get(comb) is None:
                        comb = (comb[1], comb[0])
                    if attr == "fold_changes":
                        sizes, na_keys = _get_sizes_report_nas_(self.lipid_attributes[attr][comb],
                                                                node_names,
                                                                as_abs=True,
                                                                default=np.nan)
                    else:
                        sizes, na_keys = _get_sizes_report_nas_(self.lipid_attributes[attr][comb],
                                                                node_names,
                                                                default=np.nan)
                    if not self._discrete_map_[attr]:
                        for attr_name, vmax in zip(
                                [f"{attr}_size_{_tuple_to_string_(comb)}_individual",
                                 f"{attr}_size_{_tuple_to_string_(comb)}_common"],
                                [None, max_]):
                            if attr == 'fold_changes' or attr == "nlog_pvalues":
                                attr_size = self._scale_dict_(sizes, scale,
                                                              map_as_ex=True,
                                                              vmax=vmax,
                                                              map_data_names=self.lipid_mapping)
                            else:
                                attr_size = self._scale_dict_(sizes, scale,
                                                              map_as_ex=True,
                                                              vmax=vmax)
                            if na_keys:
                                for node, val in attr_size[0].items():
                                    if np.isnan(val):
                                        attr_size[0][node] = scale[0] / 2
                            nx.set_node_attributes(
                                self.network, attr_size[0],
                                name=attr_name
                            )
                            legends_maps[attr_name] = attr_size[1]
                    else:
                        attr_size = self._scale_dict_(sizes, scale,
                                                      map_as_ex=True)
                        if na_keys:
                            for node, val in attr_size[0].items():
                                if np.isnan(val):
                                    attr_size[0][node] = scale[0] / 2
                        nx.set_node_attributes(
                            self.network, attr_size[0],
                            name=f"{attr}_size_{_tuple_to_string_(comb)}"
                        )
                        legends_maps[f"{attr}_size_{_tuple_to_string_(comb)}"] = attr_size[1]
        return legends_maps

    def dynamic_network(
        self, node_colour_attributes: List[str],
        edge_colour_attributes: List[str],
        node_size_attributes: List[str],
        node_cmaps: Dict[str, str] = None,
        edge_cmaps: Dict[str, str] = None,
        node_size_scale: Tuple[int, int] = (10, 40),
        **kwargs
    ) -> DynamicVisParser:
        """
        Generating DynamicVisParser instance to plot the interactive network
        including all available visualisation options

        :param node_colour_attributes: List[str]
            List of node colour attributes to include. For available attributes
            use linex2.node_colour_options()
        :param edge_colour_attributes: List[str]
            List of edge colour attributes to include. For available attributes
            use linex2.edge_colour_options()
        :param node_size_attributes: List[str]
            List of node size attributes to include. For available attributes
            use linex2.node_size_options()
        :param node_cmaps: Dict[str, str]
            Specifying the color maps to use for individual node attributes. Dict
            keys are attributes, values are matplotlib-compatible color maps names.
        :param edge_cmaps: Dict[str, str]
            Specifying the color maps to use for individual edge attributes. Dict
            keys are attributes, values are matplotlib-compatible color maps names.
        :param node_size_scale: Tuple[int, int], default: (10, 40)
            Scale, as a 2-tuple of (min, max), indicating the minimum and maximum
            node size value for visualisation.
        :param kwargs
            Keyword arguments passed to the DynamicVisParser initialisation function
        """
        # adding static properties
        for node_prop in STATIC_NODE_PROPERTIES.difference('enzyme_gene_name', 'enzyme_uniprot', 'enzyme_id'):
            if node_prop not in node_colour_attributes:
                node_colour_attributes.append(node_prop)
            if node_prop != "lipid_class":
                if node_prop not in node_size_attributes:
                    node_size_attributes.append(node_prop)
        for edge_prop in STATIC_EDGE_PROPERTIES.difference('enzyme_gene_name', 'enzyme_uniprot', 'enzyme_id'):
            # reaction enzymes should not get any colours!
            if edge_prop != "enzyme_id":
                if edge_prop not in edge_colour_attributes:
                    edge_colour_attributes.append(edge_prop)
        # generating colours and adding to network attributes
        node_colour_legends = self.add_network_colours(node_colour_attributes,
                                                       nodes=True, cmaps=node_cmaps)
        edge_colour_legends = self.add_network_colours(edge_colour_attributes,
                                                       nodes=False, cmaps=edge_cmaps)
        node_size_legends = self.add_node_sizes(node_size_attributes, node_size_scale)

        dvp = DynamicVisParser(**kwargs)
        dvp.from_nx(self.network)
        if dvp.directed:
            dvp.set_edge_smooth("dynamic")
        dvp.generate_legend(
            node_colours=node_colour_legends,
            edge_colours=edge_colour_legends,
            node_sizes=node_size_legends,
            colours_to_hex=True
        )
        return dvp
