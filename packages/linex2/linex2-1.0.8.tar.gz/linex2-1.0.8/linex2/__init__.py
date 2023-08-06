import matplotlib
from .lipid import Lipid, FA
from .reference import ReferenceLipid, parse_lipid_reference_table, check_reference, parse_lipid_reference_table_dict
from .validation import reaction_validator
from .reaction import Reaction, FAReaction
from .edgelist import Edge, Edgelist, reaction_str, enzyme_str
from .reaction_evaluation import Extender
from .GenerateLipidNetwork import GenerateLipidNetwork
from .parser import parse_fa_reactions, parse_excluded_fa_reactions, fa_parser, \
    parse_fatty_acids, save_lipidlynxx_converter, lipid_parser, parse_lipid_list

from .LipidNetwork import LipidNetwork
from .vis_utils import STATIC_NODE_PROPERTIES
from ._network_lipidome_summary import plot_pca, plot_heatmap


# utilities to show available attributes for plotting
def node_colour_options() -> set:
    return LipidNetwork._allowed_node_attributes_ - STATIC_NODE_PROPERTIES


def edge_colour_options() -> set:
    return LipidNetwork._allowed_edge_attributes_


def node_size_options() -> set:
    return {
        attr for attr in
        LipidNetwork._allowed_node_attributes_ - STATIC_NODE_PROPERTIES
        if not LipidNetwork._discrete_map_.get(attr, True)
    }


# Temporary functions for parsing curated Reactome and Rhea tables
from .tmp_dirty_functions import make_organism_reaction_list_from_reactome, make_all_reaction_list_from_reactome, \
    extender, make_all_reaction_list_from_rhea

