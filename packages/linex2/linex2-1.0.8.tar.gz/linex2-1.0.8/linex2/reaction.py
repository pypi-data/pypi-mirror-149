from __future__ import annotations
from typing import List
from .reference import ReferenceLipid
from .validation import reaction_validator
from .reaction_types import *
from .lipid import Lipid, FA


class Reaction:

    __slots__ = ["_substrates",
                 "_products",
                 "_Rtype",
                 "_enzymeIDs",
                 "_nl_participants",
                 "_uniprot",
                 "_gene_name"
                 ]

    def __init__(self,
                 substrates: List[ReferenceLipid],
                 products: List[ReferenceLipid],
                 reaction_type: str,
                 enzyme_ids: str,
                 non_lipid_reaction_participants: List[str],
                 uniprot: str = "",
                 gene_name: str = ""
                 ):
        self._substrates = substrates
        self._products = products
        self._Rtype = reaction_type
        self._enzymeIDs = enzyme_ids
        self._nl_participants = non_lipid_reaction_participants
        self._uniprot = uniprot
        if gene_name == "-":
            self._gene_name = ""
        self._gene_name = ", ".join(list(set(gene_name.upper().split(", "))))

    def is_valid(self, verbose=True) -> bool:
        return reaction_validator(self._Rtype, self._substrates, self._products, verbose=verbose)

    def shape(self) -> tuple:
        return len(self._substrates), len(self._products)

    def participation_equality(self, other: Reaction) -> bool:
        mysubs = sorted([x.get_abbr() for x in self._substrates])
        myprods = sorted([x.get_abbr() for x in self._products])
        osubs = sorted([x.get_abbr() for x in other._substrates])
        oprods = sorted([x.get_abbr() for x in other._products])

        return ((mysubs == osubs) and (myprods == oprods)) or ((mysubs == oprods) and (myprods == osubs))

    def subs_eq_prods(self) -> bool:
        mysubs = sorted([x.get_abbr() for x in self._substrates])
        myprods = sorted([x.get_abbr() for x in self._products])
        return mysubs == myprods

    def __eq__(self, other: Reaction) -> bool:
        return self.participation_equality(other) and self._Rtype == other._Rtype

    def extend_enzyme_ids(self, new_id: str):
        if new_id != "" and new_id is not None and new_id != "-":
            self._enzymeIDs += f";{new_id}"

    def extend_uniprot(self, new_id: str):
        if new_id != "" and new_id is not None and new_id != "-":
            if self._uniprot == "":
                self._uniprot = new_id
            else:
                self._uniprot += f", {new_id}"
            self._uniprot = ", ".join(list(set(self._uniprot.upper().split(", "))))

    def extend_gene_name(self, new_id: str):
        if new_id != "" and new_id is not None and new_id != "-":
            self._gene_name += f", {new_id}"
            self._gene_name = ", ".join(list(set(self._gene_name.upper().split(", "))))

    def extend_nl_participants(self, new_p: List[str]):
        self._nl_participants = list(set(self._nl_participants + new_p))

    def __str__(self) -> str:
        val = "Valid" if self.is_valid() else "Not-valid"
        return val + " reaction " + self._Rtype + ": " + str([x.get_abbr() for x in self._substrates])  + " <=> " + \
                     str([x.get_abbr() for x in self._products]) + " (" + self._enzymeIDs + ")"

    def reaction_nice_str(self) -> str:
        tmp = "Reaction " + self._Rtype + ":\n" + str([x.get_abbr() for x in self._substrates]) + " <=> " + \
               str([x.get_abbr() for x in self._products])
        if len(self.get_gene_name()) > 0:
            tmp += "\n(" + self.get_gene_name() + ")"
        tmp += "\n(" + self._enzymeIDs + ")"
        return tmp

    def get_reaction_type(self) -> str:
        return self._Rtype

    def get_enzyme_id(self) -> str:
        return self._enzymeIDs

    def get_enzyme_repr(self) -> str:
        if self._gene_name == "" or self._gene_name is None:
            return self._enzymeIDs
        else:
            return self._gene_name + "\n" + self._enzymeIDs

    def get_substrates(self) -> List[ReferenceLipid]:
        return self._substrates

    def get_products(self) -> List[ReferenceLipid]:
        return self._products

    def get_nl_participants(self) -> List[str]:
        return self._nl_participants

    def get_uniprot(self) -> str:
        return self._uniprot

    def get_gene_name(self) -> str:
        return self._gene_name

    def short_str(self, str_len=100, nice=False) -> str:
        if nice:
            tmp_str = self.reaction_nice_str()
        else:
            tmp_str = self.__str__()
        if len(tmp_str) > str_len:
            return tmp_str[0:str_len]+"..."
        else:
            return tmp_str


class FAReaction:

    __slots__ = ["__C", "__DB", "__OH", "__valid_ether", "__valid_lcb", "__last_conversion", "__reaction_name"]

    def __init__(self, c: int, db: int, oh: int, valid_for_ether: bool, valid_for_lcb, name: str = ""):
        self.__C = c
        self.__DB = db
        self.__OH = oh
        self.__valid_ether = valid_for_ether
        self.__valid_lcb = valid_for_lcb
        self.__last_conversion = ""
        self.__reaction_name = name

    def get_c(self) -> int:
        return self.__C

    def get_db(self) -> int:
        return self.__DB

    def get_oh(self) -> int:
        return self.__OH

    def valid_for_ether(self) -> bool:
        return self.__valid_ether

    def valid_for_lcb(self) -> bool:
        return self.__valid_lcb

    def get_name(self) -> str:
        return self.__reaction_name

    def is_transformable(self, l1: Lipid, l2: Lipid, excluded_reactions: List[List[FA]] = None) -> bool:

        if not l1.is_molecular_species() or not l2.is_molecular_species():
            raise ValueError("All lipids for fatty acid reactions must be molecular species.")

        # Lipids must be from the same class to be transformable
        if l1.get_lipid_class() != l2.get_lipid_class():
            return False
        if (((l1.sum_length() + self.__C) != l2.sum_length()) or ((l2.sum_length() + self.__C) != l1.sum_length())) and \
            (((l1.sum_dbs() + self.__DB) != l2.sum_dbs()) or ((l2.sum_dbs() + self.__DB) != l1.sum_dbs())) and \
            (((l1.sum_ohs() + self.__OH) != l2.sum_ohs()) or ((l2.sum_ohs() + self.__OH) != l1.sum_ohs())):
            return False

        fas1 = l1.get_fas()
        fas2 = l2.get_fas()
        for fa1 in range(len(fas1)):
            for fa2 in range(len(fas2)):

                # Check for FA types
                if fas1[fa1].is_long_chain_base() != fas2[fa2].is_long_chain_base():
                    continue
                if fas1[fa1].is_ether_bond() != fas2[fa2].is_ether_bond() or \
                        fas1[fa1].get_ether_type() != fas2[fa2].get_ether_type():
                    continue

                # Other FAs must be the same
                f1c = fas1.copy()
                f2c = fas2.copy()

                del f1c[fa1]
                del f2c[fa2]
                if sorted(f1c) != sorted(f2c):
                    continue

                # Check if FA types are valid here
                if fas1[fa1].is_ether_bond() and not self.valid_for_ether():
                    continue
                if fas1[fa1].is_long_chain_base() and not self.valid_for_lcb():
                    continue

                excluded = False
                # Skip excluded reactions
                if excluded_reactions is not None:
                    for er in excluded_reactions:
                        if (fas1[fa1] == er[0] and fas2[fa2] == er[1]) or \
                                (fas1[fa1] == er[1] and fas2[fa2] == er[0]):
                            excluded = True
                            continue
                # Evaluate rule
                if not excluded:
                    if (fas1[fa1].modified_fa(self.__C, self.__DB, self.__OH) == fas2[fa2]) or \
                            (fas2[fa2].modified_fa(self.__C, self.__DB, self.__OH) == fas1[fa1]):
                        self.__last_conversion = f"{fas1[fa1]} - {fas2[fa2]}"
                        return True

        return False

    def get_last_conversion(self) -> str:
        return self.__last_conversion

    def __str__(self) -> str:
        if self.__reaction_name != "":
            return f"FAReaction: {self.__reaction_name}(C:{self.__C}, DB:{self.__DB}, OH:{self.__OH})"
        else:
            return f"FAReaction(C:{self.__C}, DB:{self.__DB}, OH:{self.__OH})"

    def __repr__(self) -> str:
        return self.__str__()
