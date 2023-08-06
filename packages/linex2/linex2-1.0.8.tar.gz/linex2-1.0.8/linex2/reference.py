import pandas as pd
import numpy as np
from typing import List, Dict
from .lipid import Lipid, FA
import itertools
import warnings
from .exceptions import ReferenceLipidError


class ReferenceLipid:

    __slots__ = ["_name", "_abbreviation", "_headgroup", "_potentialFAs", "_FAs", "_ether", "_hasLCB", "_altabb",
                 "_backbone", "_category"]

    def __init__(self, name: str, abbreviation: str, hg: str, potentialfas: int, fas: int, ether: int, haslcb: int,
                 altabb: str = None, backbone: str = "glycerol", category: str = "Glycerolipids"):
        self._name = name
        self._abbreviation = abbreviation
        self._headgroup = hg
        self._potentialFAs = potentialfas
        self._FAs = fas
        self._ether = ether
        self._hasLCB = haslcb
        self._altabb = altabb
        self._backbone = backbone
        self._category = category

        if self._FAs < (self._ether+self._hasLCB):
            raise ArithmeticError("The total number of FAs must be bigger/equal that the sum of ether + LCB FAs")

    def __str__(self) -> str:
        tmp = f"Reference class of {self._name}\n" \
              f"====\n" \
              f"* Abbreviation: {self._abbreviation}\n" \
              f"* Headgroup: {self._headgroup}\n" \
              f"* potential FAs: {self._potentialFAs}\n" \
              f"* FAs: {self._FAs}\n" \
              f"* Ehter bonds: {self._ether}\n" \
              f"* Has LCB: {self._hasLCB}\n" \
              f"* Alternative Abbreviation: {self._altabb}"
        return tmp

    def __repr__(self) -> str:
        return f"Reference class of {self._name}"

    def is_of_class(self, lipid: Lipid) -> bool:
        return (lipid.get_number_fas() == self._FAs) and (lipid.get_headgroup().lower() == self._headgroup.lower()) \
                and (lipid.get_lipid_class().lower() == self._abbreviation.lower()) and \
                (lipid.get_number_long_chain_base() == self._hasLCB) and (self._ether == lipid.get_ether())

    def get_name(self) -> str:
        return self._name

    def get_abbr(self) -> str:
        return self._abbreviation

    def get_headgroup(self) -> str:
        return self._headgroup

    def get_potentialfas(self) -> int:
        return self._potentialFAs

    def get_fas(self) -> int:
        return self._FAs

    def get_ether(self) -> int:
        return self._ether

    def get_lcb(self) -> int:
        return self._hasLCB

    def get_all_abbr(self) -> list:
        if (self._altabb is None) or (self._altabb == ""):
            return [self._abbreviation]
        else:
            return [self._abbreviation] + self._altabb.split("/")

    def get_backbone(self) -> str:
        return self._backbone

    def get_category(self) -> str:
        return self._category


def check_reference(lipid: Lipid, reference: ReferenceLipid, throw_error: bool = False) -> Lipid:
    if not reference.is_of_class(lipid):
        if throw_error:
            raise ReferenceLipidError(f"{str(lipid)} does not match with Reference class ({repr(reference)})")
        else:
            warnings.warn(f"{str(lipid)} does not match with Reference class ({repr(reference)})")

    return lipid


def parse_lipid_reference_table(tab: pd.DataFrame) -> List[ReferenceLipid]:

    return_l = []

    for row in range(tab.shape[0]):
        if bool(tab["Lipid Class"][row]):

            if tab["Lipid class"][row] is np.nan:
                raise KeyError("Each lipid class needs a name")
            else:
                dummy_name = str(tab["Lipid class"][row])

            if tab["Abbreviation"][row] is np.nan:
                raise KeyError("Each lipid class needs an abbreviation")
            else:
                dummy_abbr = str(tab["Abbreviation"][row])

            if tab["AltAbb"][row] is np.nan:
                dummy_altabb = ""
            else:
                dummy_altabb = str(tab["AltAbb"][row])

            if tab["HeadGroup"][row] is np.nan:
                dummy_hg = ""
            else:
                dummy_hg = str(tab["HeadGroup"][row]).upper()

            if tab["PotentialFAs"][row] is np.nan:
                dummy_pFA = 0
            else:
                dummy_pFA = int(tab["PotentialFAs"][row])

            if tab["FAs"][row] is np.nan:
                dummy_fas = 0
            else:
                dummy_fas = int(tab["FAs"][row])

            if tab["Ether"][row] is np.nan:
                dummy_ether = 0
            else:
                dummy_ether = int(tab["Ether"][row])

            if tab["has_long_chain_base"][row] is np.nan:
                dummy_lcb = 0
            else:
                dummy_lcb = int(tab["has_long_chain_base"][row])

            if tab["backbone"][row] is np.nan:
                dummy_backbone = "glycerol"
            else:
                dummy_backbone = str(tab["backbone"][row])

            if tab["Lipid category"][row] is np.nan:
                dummy_category = ""
            else:
                dummy_category = str(tab["Lipid category"][row])

            return_l.append(ReferenceLipid(name=dummy_name,
                                           abbreviation=dummy_abbr,
                                           hg=dummy_hg,
                                           potentialfas=dummy_pFA,
                                           fas=dummy_fas,
                                           ether=dummy_ether,
                                           haslcb=dummy_lcb,
                                           altabb=dummy_altabb,
                                           backbone=dummy_backbone,
                                           category=dummy_category))

    return return_l


def parse_lipid_reference_table_dict(tab: pd.DataFrame) -> Dict[str, ReferenceLipid]:
    tmp_list = parse_lipid_reference_table(tab)
    out_dict = {}
    for rl in tmp_list:
       for abb in rl.get_all_abbr():
           if abb in out_dict.keys():
               raise KeyError(f"Abbreviation '{abb}' already in use for another lipid.")
           out_dict[abb.upper()] = rl
    return out_dict


# def generate_reference_lipids_list(rl: List[ReferenceLipid], fa: List[FA], lcb: List[FA],
#                                    ether: List[FA]) -> List[Lipid]:
#     return_l = []
#
#     for f in fa:
#         if f.is_long_chain_base():
#             raise KeyError("Fatty Acids cannot be a long chain base")
#         if f.is_ether_bond():
#             raise KeyError("Fatty acid cannot be an ether bond")
#
#     for l in lcb:
#         if not l.is_long_chain_base():
#             raise KeyError("LCB has to be a LCB")
#         if l.is_ether_bond():
#             raise KeyError("LCB cannot be an ether bond")
#
#     for e in ether:
#         if not e.is_ether_bond():
#             raise KeyError("Ether FAs have to be ether")
#         if e.is_long_chain_base():
#             raise KeyError("Ether FA cannot be a LCB")
#
#     for lipid in rl:
#         n_fa = lipid.get_fas()
#         n_lcb = lipid.get_lcb()
#         n_ether = lipid.get_ether()
#
#         if (n_lcb == 0) and (n_ether == 0):
#             if len(fa) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one FA.")
#             combs = list(itertools.combinations_with_replacement(fa, n_fa))
#             for i in combs:
#                 return_l.append(Lipid(lipid_class=lipid.get_abbr(),
#                                       head_group=lipid.get_headgroup(),
#                                       is_molecular_species=True,
#                                       fa_spots=lipid.get_potentialfas(),
#                                       fatty_acids=list(i)))
#         elif (n_lcb == 0) and (n_ether != 0):
#             if len(fa) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one FA.")
#             if len(ether) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one ether FA.")
#
#             combs_fa = list(itertools.combinations_with_replacement(fa, n_fa-n_ether))
#             combs_ether = list(itertools.combinations_with_replacement(ether, n_ether))
#
#             for cf in combs_fa:
#                 for ce in combs_ether:
#                     return_l.append(Lipid(lipid_class=lipid.get_abbr(),
#                                           head_group=lipid.get_headgroup(),
#                                           is_molecular_species=True,
#                                           fa_spots=lipid.get_potentialfas(),
#                                           fatty_acids=list(cf)+list(ce)))
#
#         elif (n_lcb != 0) and (n_ether == 0):
#             if len(fa) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one FA.")
#             if len(lcb) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one LCB.")
#
#             combs_fa = list(itertools.combinations_with_replacement(fa, n_fa-n_lcb))
#             combs_lcb = list(itertools.combinations_with_replacement(lcb, n_lcb))
#
#             for cf in combs_fa:
#                 for cl in combs_lcb:
#                     return_l.append(Lipid(lipid_class=lipid.get_abbr(),
#                                           head_group=lipid.get_headgroup(),
#                                           is_molecular_species=True,
#                                           fa_spots=lipid.get_potentialfas(),
#                                           fatty_acids=list(cf)+list(cl)))
#         else:
#             if len(fa) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one FA.")
#             if len(lcb) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one LCB.")
#             if len(ether) == 0:
#                 raise ArithmeticError(f"Lipid {lipid.get_abbr()} requires at least one ether FA.")
#
#             combs_fa = list(itertools.combinations_with_replacement(fa, n_fa - n_lcb))
#             combs_lcb = list(itertools.combinations_with_replacement(lcb, n_lcb))
#             combs_ether = list(itertools.combinations_with_replacement(ether, n_ether))
#
#             for cf in combs_fa:
#                 for cl in combs_lcb:
#                     for ce in combs_ether:
#                         return_l.append(Lipid(lipid_class=lipid.get_abbr(),
#                                               head_group=lipid.get_headgroup(),
#                                               is_molecular_species=True,
#                                               fa_spots=lipid.get_potentialfas(),
#                                               fatty_acids=list(cf) + list(cl)+list(ce)))
#
#     return return_l
#
#
# def generate_reference_lipids_dict(rl: List[ReferenceLipid], fa: List[FA], lcb: List[FA],
#                                    ether: List[FA]) -> Dict[str, List[Lipid]]:
#
#     tmp_l = generate_reference_lipids_list(rl, fa, lcb, ether)
#
#     out_dict = {}
#
#     for i in tmp_l:
#         if i.get_lipid_class() in out_dict.keys():
#             out_dict[i.get_lipid_class()].append(i)
#         else:
#             out_dict[i.get_lipid_class()] = [i]
#
#     return out_dict
