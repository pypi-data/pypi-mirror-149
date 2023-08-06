from __future__ import annotations
from typing import List
from .lipid import Lipid, FA
from .reference import ReferenceLipid
from .reaction import Reaction, FAReaction
from datetime import datetime


class Edge:

    __slots__ = ["__l1",
                 "__l2",
                 "__enzyme_id",
                 "__reaction_id",
                 "__reaction_type",
                 "__notes",
                 "__enzyme_uniprot",
                 "__enzyme_gene_name",
                 "__reaction_structure", # 1,1; 1,2; 2,2
                 "__l1_type",
                 "__l2_type",
                 "__set_id",
                 "__fa_param",
                 "__nl_participants"]

    def __init__(self, l1: Lipid, l2: Lipid, enzyme_id: str,
                 reaction_id: str, reaction_type: str, notes: str,
                 uniprot: str = "", gene_name: str = "",
                 reaction_structure: str = "1,1",
                 l1_type: str = "substrate",
                 l2_type: str = "product",
                 set_id: int = 0,
                 fa_param: str = "",
                 nl_participants: List[str] = None):
        if enzyme_id == None:
            raise ValueError("Enzyme ID cannot be None")
        self.__l1 = l1
        self.__l2 = l2
        self.__enzyme_id = enzyme_id
        self.__reaction_type = reaction_type
        self.__reaction_id = reaction_id
        self.__notes = notes
        self.__enzyme_gene_name = gene_name
        self.__enzyme_uniprot = uniprot
        self.__reaction_structure = reaction_structure
        self.__l1_type = l1_type
        self.__l2_type = l2_type
        self.__set_id = set_id
        self.__fa_param = fa_param
        if nl_participants is None:
            self.__nl_participants = []
        else:
            self.__nl_participants = nl_participants

    def get_l1(self) -> Lipid:
        return self.__l1

    def get_l2(self) -> Lipid:
        return self.__l2

    def get_enzyme_id(self, nlen=100, full=False) -> str:
        if full:
            return self.__enzyme_id
        elif len(self.__enzyme_id) > nlen:
            return self.__enzyme_id[0:nlen] + "..."
        else:
            return self.__enzyme_id

    def get_fa_param(self) -> str:
        return self.__fa_param

    def get_enzyme_repr(self, nlen=100) -> str:
        if self.__enzyme_gene_name == "" or self.__enzyme_gene_name is None:
            if len(self.get_enzyme_id()) > nlen:
                return self.get_enzyme_id()[0:nlen] + "..."
            else:
                return self.get_enzyme_id()
        else:
            return self.__enzyme_gene_name[0:nlen] + "..."

    def get_enzyme_uniprot(self) -> str:
        return self.__enzyme_uniprot

    def get_enzyme_gene_name(self) -> str:
        return self.__enzyme_gene_name

    def get_reaction_type(self) -> str:
        return self.__reaction_type

    def get_reaction_id(self) -> str:
        return self.__reaction_id

    def get_notes(self) -> str:
        return self.__notes

    def get_reaction_structure(self) -> str:
        return self.__reaction_structure

    def get_l1_type(self) -> str:
        return self.__l1_type

    def get_l2_type(self) -> str:
        return self.__l2_type

    def get_set_id(self) -> int:
        return self.__set_id

    def get_nl_participants(self) -> List[str]:
        return self.__nl_participants

    def __str__(self) -> str:

        # tmp_l = sorted([str(self.__l1), str(self.__l2)])
        return f"{str(self.__l1)} - {str(self.__l2)} [{self.__reaction_type}; {self.__reaction_id}, " \
               f"{self.get_enzyme_repr()}, {self.__notes}, {self.__reaction_structure}]"

    def sum_species_str(self) -> str:
        # tmp_l = sorted([self.__l1.sum_species_str(), self.__l2.sum_species_str()])
        return f"{str(self.__l1)} - {str(self.__l2)} [{self.__reaction_type}; {self.__reaction_id}, " \
               f"{self.get_enzyme_repr()}, {self.__notes}, {self.__reaction_structure}]"

    def native_str(self) -> str:
        tmp_l = [self.__l1.get_native_string(), self.__l2.get_native_string()]
        return f"{tmp_l[0]} - {tmp_l[1]} [{self.__reaction_type}; {self.__reaction_id}, " \
               f"{self.get_enzyme_repr()}, {self.__notes}, {self.__reaction_structure}]"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: Edge) -> bool:
        if self.__hash__() == hash(other):
            return True
        else:
            return False

reaction_str = "Reaction: "
enzyme_str = "Enzyme: "

def edge_attr_dict(x: Edge):
    return {
        "enzyme_id": x.get_enzyme_id(full=True),
        "reaction_type": x.get_reaction_type(),
        "reaction_id": x.get_reaction_id(),
        "notes": x.get_notes(),
        "enzyme_gene_name": x.get_enzyme_gene_name(),
        "enzyme_raw_id": x.get_enzyme_repr(),
        "enzyme_uniprot": x.get_enzyme_uniprot(),
        "reaction_structure": x.get_reaction_structure(),
        "l1_type": x.get_l1_type(),
        "l2_type": x.get_l2_type(),
        "set_id": x.get_set_id(),
        "id_fa_raw": x.get_enzyme_id() + "\nFA: " + x.get_fa_param(),
        "id_fa_param": x.get_fa_param(),
        "nl_participants": x.get_nl_participants()
    }

def lipid_edges_to_bip(el: list, bipartite_type: str = "reaction"):
    new_l = []
    if bipartite_type == "reaction":
        for e in el:
            if e[2]["reaction_id"] == "":
                new_l.append(e)
            else:

                new_l.append([e[0], reaction_str + e[2]["reaction_id"], dict(e[2], enzyme_edge=True)])
                new_l.append([e[1], reaction_str + e[2]["reaction_id"], dict(e[2], enzyme_edge=True)])

        return new_l

    elif bipartite_type == "enzyme":
        for e in el:
            if e[2]["enzyme_id"] == "":
                new_l.append(e)
            else:
                new_l.append([e[0], enzyme_str + e[2]["enzyme_id"], dict(e[2], enzyme_edge=True)])
                new_l.append([e[1], enzyme_str + e[2]["enzyme_id"], dict(e[2], enzyme_edge=True)])

        return new_l

    elif bipartite_type == "hyper":
        for e in el:
            # Non hyper edges
            f = e[2].copy()
            if f["enzyme_id"] == "":
                f["hyper"] = False
                new_l.append([e[0], e[1], dict(f, enzyme_edge=False)])
            # Hyper edges
            else:
                f["hyper"] = True
                new_l.append([e[0], enzyme_str + f["enzyme_id"], dict(f, enzyme_edge=True)])
                new_l.append([e[1], enzyme_str + f["enzyme_id"], dict(f, enzyme_edge=True)])
                new_l.append([e[0], e[1], dict(f, enzyme_edge=False)])

        return new_l

    else:
        raise ValueError("'bipartite_type' must be one of ('reaction', 'enzyme', 'hyper')")

class Edgelist:

    __slots__ = ["__edges"]

    def __init__(self, edges: List[Edge] = None):
        if edges is None:
            self.__edges = []
        else:
            self.__edges = edges

    def raw_edgelist_copy(self) -> List[Edge]:
        return self.__edges.copy()

    def raw_enzymes(self) -> List[str]:
        return [x.get_enzyme_repr() for x in self.__edges]

    def raw_reaction_ids(self) -> List[str]:
        return [x.get_reaction_id() for x in self.__edges]

    def raw_edge_notes(self) -> List[str]:
        return [x.get_notes() for x in self.__edges]

    def raw_edge_types(self) -> List[str]:
        return [x.get_reaction_type() for x in self.__edges]

    def add_edge(self, edge: Edge):
        self.__edges.append(edge)

    def add_edges(self, edges: List[Edge]):
        self.__edges += edges

    def __add__(self, other: Edgelist):
        return Edgelist(edges=self.raw_edgelist_copy()+other.raw_edgelist_copy())

    def molecular_species_edgelist(self, filter_duplicates: bool = False,
                                   excluded_reaction_types: List[str] = None,
                                   bipartite: bool = False, bipartite_type: str = "reaction") -> List:
        """

        :param filter_duplicates:
        :param excluded_reaction_types:
        :param bipartite:
        :param bipartite_type: "reaction" or "enzyme"
        :return:
        """

        if not filter_duplicates:
            if excluded_reaction_types is None:
                return_l = [[str(x.get_l1()), str(x.get_l2()), edge_attr_dict(x)] for x in self.__edges]

            else:
                return_l = [[str(x.get_l1()), str(x.get_l2()), edge_attr_dict(x)] for x in self.__edges if
                        x.get_reaction_type() not in excluded_reaction_types]
        else:
            tmp_e = set(self.__edges)
            if excluded_reaction_types is None:
                return_l = [[str(x.get_l1()), str(x.get_l2()), edge_attr_dict(x)] for x in tmp_e]
            else:
                return_l = [[str(x.get_l1()), str(x.get_l2()), edge_attr_dict(x)] for x in tmp_e if
                        x.get_reaction_type() not in excluded_reaction_types]

        if not bipartite:
            return return_l
        else:
            return lipid_edges_to_bip(return_l, bipartite_type=bipartite_type)


    def __native_set(self) -> List[Edge]:
        unique_edges = []
        unique_edge_str = []
        for e in self.__edges:
            if e.native_str() in unique_edge_str:
                pass
            else:
                unique_edge_str.append(e.native_str())
                unique_edges.append(e)

        return unique_edges

    def native_edgelist(self, filter_duplicates: bool = False,
                        excluded_reaction_types: List[str] = None,
                                   bipartite: bool = False, bipartite_type: str = "reaction") -> List:
        start = datetime.now()
        if not filter_duplicates:
            if excluded_reaction_types is None:
                return_l = [[str(x.get_l1().get_native_string()), str(x.get_l2().get_native_string()),
                         edge_attr_dict(x)] for x in self.__edges]
            else:
                return_l = [[str(x.get_l1().get_native_string()), str(x.get_l2().get_native_string()),
                         edge_attr_dict(x)] for x in self.__edges if
                        x.get_reaction_type() not in excluded_reaction_types]
        else:
            tmp_e = self.__native_set()
            if excluded_reaction_types is None:
                return_l = [[str(x.get_l1().get_native_string()), str(x.get_l2().get_native_string()),
                         edge_attr_dict(x)] for x in tmp_e]
            else:
                return_l = [[str(x.get_l1().get_native_string()), str(x.get_l2().get_native_string()),
                         edge_attr_dict(x)] for x in tmp_e if
                        x.get_reaction_type() not in excluded_reaction_types]
        if not bipartite:
            return return_l
        else:
            tmp = lipid_edges_to_bip(return_l, bipartite_type=bipartite_type)
            return tmp

    def __sum_species_set(self) -> List[Edge]:
        unique_edges = []
        unique_edge_str = []
        for e in self.__edges:
            if e.sum_species_str() in unique_edge_str:
                pass
            else:
                unique_edge_str.append(e.sum_species_str())
                unique_edges.append(e)

        return unique_edges

    def sum_species_edgelist(self, filter_duplicates=False, excluded_reaction_types: List[str] = None,
                                   bipartite: bool = False, bipartite_type: str = "reaction") -> List:

        if not filter_duplicates:
            if excluded_reaction_types is None:
                return_l = [[x.get_l1().sum_species_str(), x.get_l2().sum_species_str(),
                         edge_attr_dict(x)] for x in self.__edges]
            else:
                return_l = [[x.get_l1().sum_species_str(), x.get_l2().sum_species_str(),
                         edge_attr_dict(x)] for x in self.__edges if
                        x.get_reaction_type() not in excluded_reaction_types]
        else:
            tmp_e = self.__sum_species_set()
            if excluded_reaction_types is None:
                return_l = [[x.get_l1().sum_species_str(), x.get_l2().sum_species_str(),
                         edge_attr_dict(x)] for x in tmp_e]
            else:
                return_l = [[x.get_l1().sum_species_str(), x.get_l2().sum_species_str(),
                         edge_attr_dict(x)] for x in tmp_e if
                        x.get_reaction_type() not in excluded_reaction_types]
        if not bipartite:
            return return_l
        else:
            return lipid_edges_to_bip(return_l, bipartite_type=bipartite_type)

    def __str__(self) -> str:
        return f"Edgelist with {len(self.__edges)} edges."

    def __len__(self) -> int:
        return len(self.__edges)
