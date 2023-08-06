import warnings

from .reference import ReferenceLipid
from .lipid import Lipid, FA
from .reaction import Reaction, FAReaction
from typing import List, Dict, Union, Tuple
from .edgelist import Edgelist, reaction_str, enzyme_str
from .reaction_evaluation import Extender
from .exceptions import MappingError, MolecularSpeciesError
from .utils import reaction_titles, get_class_reaction
import networkx as nx


def lipid_attributes(lipid: Lipid) -> Dict[str, Union[str, int, float]]:
    if lipid.get_number_fas() == 0:
        # avoid zero division
        return {
            "node_molecule_type": "Lipid", "data_name": lipid.get_dataname(), "lipid_class": lipid.get_lipid_class(),
            "chain_length": lipid.sum_length(), "desaturation": lipid.sum_dbs(), "hydroxylation": lipid.sum_ohs(),
            "c_index": 0, "db_index": 0, "oh_index": 0, "inferred": lipid.converted_to_mol_spec(),
            "molecular_string": str(lipid)
        }
    return {
        "node_molecule_type": "Lipid", "data_name": lipid.get_dataname(), "lipid_class": lipid.get_lipid_class(),
        "chain_length": lipid.sum_length(), "desaturation": lipid.sum_dbs(), "hydroxylation": lipid.sum_ohs(),
        "c_index": lipid.sum_length()/lipid.get_number_fas(), "db_index": lipid.sum_dbs()/lipid.get_number_fas(),
        "oh_index": lipid.sum_ohs()/lipid.get_number_fas(), "inferred": lipid.converted_to_mol_spec(),
        "molecular_string": str(lipid)
    }


def non_lipid_attributes(node_type: str, class_reactions=None, raw_str=None):
    # TODO: add nl_pariticpants etc. here to pass to LipidNetwork
    attrs = {
        "node_molecule_type": node_type, "data_name": None, "lipid_class": "",
        "chain_length": 1, "desaturation": 0, "hydroxylation": 0,
        "c_index": 1, "db_index": 0, "oh_index": 0
    }
    if raw_str is not None:
        id_str = raw_str.split(enzyme_str)[1] if enzyme_str in raw_str else raw_str
        reaction = get_class_reaction(id_str, class_reactions)
        if reaction is None:
            warnings.warn(f'No class reaction found for {raw_str}')
        else:
            attrs["representation_id"] = reaction_titles(id_str, class_reaction=reaction)
            attrs["nl_participants"] = '; '.join(reaction.get_nl_participants())
            attrs["enzyme_ids"] = reaction.get_enzyme_id()
    return attrs


class GenerateLipidNetwork:

    __slots__ = ["__reference_lipids",
                 "__lipids",
                 "__class_reactions",
                 "__fa_reactions",
                 "__excluded_fa_reactions",
                 "__edgelist",
                 "__extender",
                 "__class_fatty_acids",
                 "__has_molecular_species",
                 "__ether_conversions"]

    def __init__(self, reference_lipids: List[ReferenceLipid],
                 lipids: Dict[str, List[Lipid]],
                 class_reactions: List[Reaction],
                 fa_reactions: List[FAReaction],
                 excluded_fa_reactions: List[List[FA]] = None,
                 class_fatty_acids: Dict[str, List[FA]] = None,
                 ether_conversions: bool = True,
                 confirmed_species_dict: Dict[str, List[Lipid]] = None):

        if confirmed_species_dict is None:
            confirmed_species_dict = dict()

        # Check if all lipids are molecular species and convert them if not.
        self.__has_molecular_species = False

        new_lipids = dict()
        molspec_error_list = []
        for i in lipids.keys():
            new_lipids[i] = list()
            for l in lipids[i]:
                if l.get_dataname() is None or l.get_dataname() == "":
                    warnings.warn(f"Lipid {str(l)} does not have a data Name, which is required for mapping!")
                if l.is_molecular_species():
                    new_lipids[i].append(l)
                    self.__has_molecular_species = True
                else:
                    if class_fatty_acids is None:
                        raise ValueError("Non molecular lipids in the data, but no class fatty acids provided."
                                         "The class_fatty_acids argument cannot be none")
                    else:
                        # Look at confirmed species
                        if i in confirmed_species_dict.keys():
                            # Loop over all confirmed species
                            tmp_ms_list = []
                            for cfs in confirmed_species_dict[i]:
                                if l.sum_species_str() == cfs.sum_species_str():
                                    cfs.set_dataname(l.get_dataname())
                                    tmp_ms_list.append(cfs)

                            if len(tmp_ms_list) > 0:
                                new_lipids[i] = new_lipids[i] + tmp_ms_list
                            else:
                                try:
                                    new_lipids[i] = new_lipids[i] + \
                                                    l.get_molecular_species(class_fatty_acids["all"] if
                                                                            l.get_lipid_class() not in class_fatty_acids else
                                                                            class_fatty_acids[l.get_lipid_class()])
                                except MolecularSpeciesError as e:
                                    molspec_error_list.append(str(e).split(" | ")[1])
                        else:
                            try:
                                new_lipids[i] = new_lipids[i] + \
                                                l.get_molecular_species(class_fatty_acids["all"] if
                                                                        l.get_lipid_class() not in class_fatty_acids else
                                                                        class_fatty_acids[l.get_lipid_class()])
                            except MolecularSpeciesError as e:
                                molspec_error_list.append(str(e).split(" | ")[1])
        if len(molspec_error_list) > 0:
            raise MolecularSpeciesError("Molecular species could not be inferred for the following lipids.\n"
                                        "Try to add more possible fatty acids in the fatty acid file.\n"
                                        f"{', '.join(molspec_error_list)}")


        self.__reference_lipids = reference_lipids
        self.__lipids = new_lipids
        self.__class_reactions = class_reactions
        self.__fa_reactions = fa_reactions
        self.__excluded_fa_reactions = excluded_fa_reactions
        self.__extender = Extender(class_reactions=class_reactions, fatty_acid_reactions=fa_reactions)
        self.__edgelist = Edgelist()
        self.__class_fatty_acids = class_fatty_acids
        self.__ether_conversions = ether_conversions

    def get_lipid_dict(self) -> Dict[str, List[Lipid]]:
        return self.__lipids

    def add_new_lipid(self, new_lipid: Lipid):
        # Convert to molecular soecies if necessary
        new_lipid.set_dataname("no_data_name")
        if new_lipid.is_molecular_species():
            l = [new_lipid]
        else:
            l = new_lipid.get_molecular_species(self.__class_fatty_acids["all"] if
                                                new_lipid.get_lipid_class() not in self.__class_fatty_acids else
                                                self.__class_fatty_acids[new_lipid.get_lipid_class()])

        if new_lipid.get_lipid_class() in self.__lipids:
            self.__lipids[new_lipid.get_lipid_class()] += l
        else:
            if len(l) > 0:
                self.__lipids[new_lipid.get_lipid_class()] = l
        self.__edgelist = Edgelist()

    def compute_edgelist(self,
                         parallel: bool = False,
                         n_cores: int = 4):
        if parallel:
            warnings.warn("Parallel edgelist computing has been temporarily disabled.\n"
                          "Edgelist will be computed on a single thread.")
            self.__edgelist = self.__extender.evaluate_all(self.__lipids,
                                                           self.__excluded_fa_reactions,
                                                           ether_conversions=self.__ether_conversions,
                                                           reference_lipids=self.__reference_lipids)
            # Disabled parallel:
            # self.__edgelist = self.__extender.evaluate_all_parallel(self.__lipids,
            #                                                         n_cores, self.__excluded_fa_reactions)
        else:
            self.__edgelist = self.__extender.evaluate_all(self.__lipids,
                                                           self.__excluded_fa_reactions,
                                                           ether_conversions=self.__ether_conversions,
                                                           reference_lipids=self.__reference_lipids)

    def molecular_species_network(self, filter_duplicates: bool = False,
                                  excluded_reaction_types: List[str] = None,
                                  return_lipid_mapping: bool = False,
                                  bipartite: bool = False,
                                  bipartite_type: str = "reaction",
                                  multi: bool = False) -> Union[nx.Graph, Tuple[nx.Graph, Dict[str, str]]]:
        if len(self.__edgelist) == 0:
            print("no edgelist available yet. Will be computed using default parameters")
            self.compute_edgelist()
        if multi:
            g = nx.MultiGraph()
        else:
            g = nx.Graph()
        ef = self.__edgelist.molecular_species_edgelist(filter_duplicates=filter_duplicates,
                                                        excluded_reaction_types=excluded_reaction_types,
                                                        bipartite=bipartite, bipartite_type=bipartite_type)
        g.add_edges_from(ef)

        node_list = []
        lipid_mapping = {}

        for lcls in self.__lipids:  # Lipid classes
            for lip in self.__lipids[lcls]:  # Lipids of one class
                node_list.append(lip)
                if lip.get_dataname() in lipid_mapping.keys():
                    lipid_mapping[lip.get_dataname()] = lipid_mapping[lip.get_dataname()] + [str(lip)]
                else:
                    lipid_mapping[lip.get_dataname()] = [str(lip)]

        node_list = list(set(node_list))
        node_list = [(str(x), lipid_attributes(x)) for x in node_list]
        tmp_enz_l = []
        if bipartite:
            if bipartite_type == "reaction":
                tmp_enz_l = [n[1] for n in ef if n[1].startswith(reaction_str)]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, non_lipid_attributes("Reaction")) for x in tmp_enz_l]
            else:
                tmp_enz_l = [n[1] for n in ef if n[1].startswith(enzyme_str)]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, non_lipid_attributes("Enzyme", self.__class_reactions, x)) for x in tmp_enz_l]

        g.add_nodes_from(node_list + tmp_enz_l)

        g.remove_edges_from(nx.selfloop_edges(g))
        if return_lipid_mapping:
            return g, lipid_mapping
        else:
            return g

    def sum_species_network(self, filter_duplicates: bool = False,
                            excluded_reaction_types: List[str] = None, force: bool = False,
                            return_lipid_mapping: bool = False, bipartite: bool = False,
                            bipartite_type: str = "reaction") -> nx.Graph:
        if not force:
            raise MappingError("Sum species network not supported anymore."
                               "The network can be enforced with the parameter force=True.")
        if len(self.__edgelist) == 0:
            print("no edgelist available yet. Will be computed using default parameters")
            self.compute_edgelist()
        g = nx.Graph()
        ef = self.__edgelist.sum_species_edgelist(filter_duplicates=filter_duplicates,
                                                  excluded_reaction_types=excluded_reaction_types,
                                                  bipartite=bipartite, bipartite_type=bipartite_type)
        g.add_edges_from(ef)
        node_list = []
        lipid_mapping = {}

        for lcls in self.__lipids:  # Lipid classes
            for lip in  self.__lipids[lcls]:  # Lipids of one class
                node_list.append((lip.sum_species_str(), {"node_molecule_type": "Lipid"}))
                if lip.get_dataname() in lipid_mapping.keys():
                    lipid_mapping[lip.get_dataname()] = lipid_mapping[lip.get_dataname()] + [lip.sum_species_str()]
                else:
                    lipid_mapping[lip.get_dataname()] = [lip.sum_species_str()]

        node_list = list(set(node_list))

        tmp_enz_l = []
        if bipartite:
            if bipartite_type == "reaction":
                tmp_enz_l = [n[1] for n in ef]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, {"node_molecule_type": "Reaction"}) for x in tmp_enz_l]
            else:
                tmp_enz_l = [n[1] for n in ef]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, {"node_molecule_type": "Enzyme"}) for x in tmp_enz_l]

        tmp_enz_l = list(set(tmp_enz_l))
        g.add_nodes_from(node_list + tmp_enz_l)

        if return_lipid_mapping:
            return g, lipid_mapping
        else:
            return g

    def native_network(self, filter_duplicates: bool = False,
                       excluded_reaction_types: List[str] = None,
                       return_lipid_mapping: bool = False,
                       bipartite: bool = False,
                       bipartite_type: str = "reaction",
                       recompute_edgelist: bool = False,
                       multi: bool = False) -> Union[nx.Graph, Tuple[nx.Graph, Dict[str, str]]]:

        if len(self.__edgelist) == 0 or recompute_edgelist:
            print("no edgelist available yet. Will be computed using default parameters")
            self.compute_edgelist()
        if multi:
            g = nx.MultiGraph()
        else:
            g = nx.Graph()
        ef = self.__edgelist.native_edgelist(filter_duplicates=filter_duplicates,
                                                         excluded_reaction_types=excluded_reaction_types,
                                             bipartite=bipartite, bipartite_type=bipartite_type)
        g.add_edges_from(ef)

        node_list = []
        lipid_mapping = {}

        for lcls in self.__lipids:  # Lipid classes
            for lip in self.__lipids[lcls]:  # Lipids of one class
                node_list.append(lip)
                if lip.get_dataname() in lipid_mapping.keys():
                    if lip.get_native_string() not in lipid_mapping[lip.get_dataname()]:
                        lipid_mapping[lip.get_dataname()] = lipid_mapping[lip.get_dataname()] + [lip.get_native_string()]
                else:
                    lipid_mapping[lip.get_dataname()] = [lip.get_native_string()]

        node_list = list(set(node_list))
        node_list = [(x.get_native_string(), lipid_attributes(x)) for x in node_list]
        tmp_enz_l = []
        if bipartite:
            if bipartite_type == "reaction":
                tmp_enz_l = [n[1] for n in ef if n[1].startswith(reaction_str)]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, non_lipid_attributes("Reaction")) for x in tmp_enz_l]
            else:
                tmp_enz_l = [n[1] for n in ef if n[1].startswith(enzyme_str)]
                tmp_enz_l = list(set(tmp_enz_l))
                tmp_enz_l = [(x, non_lipid_attributes("Enzyme", self.__class_reactions, x)) for x in tmp_enz_l]
        g.add_nodes_from(node_list + tmp_enz_l)
        g.remove_edges_from(nx.selfloop_edges(g))

        if return_lipid_mapping:
            return g, lipid_mapping
        else:
            return g

    def len_edgelist(self) -> int:
        return len(self.__edgelist)

    @property
    def n_lipids(self) -> int:
        return len(self.__lipids)

    def get_class_reactions(self) -> List[Reaction]:
        return self.__class_reactions

    def _get_edgelist(self) -> Edgelist:
        return self.__edgelist
