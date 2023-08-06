# ###
# Classes for lipids that will be used for the dynamic network creation
# ###
from __future__ import annotations
import warnings
from typing import List
import itertools
from .exceptions import MolecularSpeciesError

class FA:

    __slots__ = ["__C", "__DB", "__OH", "__modifications", "__is_long_chain_base", "__is_ether_bond", "__ether_type"]

    def __init__(self, c: int, db: int, oh: int = None, modifications: list = None,
                 is_long_chain_base: bool = False, is_ether_bond: bool = False, ether_type: str = None):
        """
        Fatty acid class. Describes a fatty acid that can be part of a Lipid
        :param c: int, Number of carbons
        :param db: int, Number of double bonds
        :param oh: int, Number of hydroxylations, can be None.
        :param modifications: List of string, Other modifications of the fatty acid
        """
        self.__C = c
        self.__DB = db
        if oh is None:
            self.__OH = 0
        else:
            self.__OH = oh
        self.__modifications = modifications
        self.__is_long_chain_base = is_long_chain_base
        self.__is_ether_bond = is_ether_bond
        if self.__is_ether_bond and ether_type is None:
            self.__ether_type = "O-"
        else:
            self.__ether_type = ether_type

        if self.__ether_type is not None:
            self.__ether_type = self.__ether_type.upper()

        if modifications is not None:
            self.__modifications.sort()

        if self.__is_long_chain_base and self.__is_ether_bond:
            warnings.warn("Fatty acid is long chain base and ether bond at once.")

    def length(self) -> int:
        return self.__C

    def db_index(self) -> int:
        return self.__DB

    def hydroxylations(self) -> int:
        return self.__OH

    def modifications(self) -> List:
        return self.__modifications

    def is_long_chain_base(self) -> bool:
        return self.__is_long_chain_base

    def is_ether_bond(self) -> bool:
        return self.__is_ether_bond

    def get_ether_type(self) -> str:
        return self.__ether_type

    def __eq__(self, other) -> bool:
        if not isinstance(other, FA):
            raise TypeError("Only comparisons between FAs allowed.")
        return (self.__C == other.length()) & (self.__DB == other.db_index()) &\
               (self.__OH == other.hydroxylations()) & (self.__modifications == other.modifications()) &\
               (self.__is_long_chain_base == other.is_long_chain_base()) &\
               (self.__is_ether_bond == other.is_ether_bond())

    def __str__(self) -> str:
        out_str = ""
        if self.__is_ether_bond:
            out_str += self.__ether_type
        # if self.__is_long_chain_base:
        #     out_str += "d"
        out_str += f"{self.__C}:{self.__DB}"
        if self.__OH:
            if self.__OH > 1:
                out_str += f";O{self.__OH}"
            else:
                out_str += f";O"
        return out_str

    def __hash__(self):
        return hash("l" + str(self)) # Mark as LCB for hashing

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other) -> bool:
        if (not self.__is_long_chain_base) and other.is_long_chain_base():
            return False
        elif self.__is_long_chain_base and (not other.is_long_chain_base()):
            return True
        elif (not self.__is_ether_bond) and other.is_ether_bond():
            return False
        elif self.__is_ether_bond and (not other.is_ether_bond()):
            return True
        else:
            if self.__C < other.length():
                return True
            elif self.__C > other.length():
                return False
            else:
                if self.__DB < other.db_index():
                    return True
                elif self.__DB > other.db_index():
                    return False
                else:
                    myoh = 0 if self.__OH is None else self.__OH
                    otheroh = 0 if other.hydroxylations() is None else other.hydroxylations()
                    if myoh < otheroh:
                        return True
                    elif myoh > otheroh:
                        return False

    def __le__(self, other) -> bool:
        if (not self.__is_long_chain_base) and other.is_long_chain_base():
            return False
        elif self.__is_long_chain_base and (not other.is_long_chain_base()):
            return True
        if (not self.__is_ether_bond) and other.is_ether_bond():
            return False
        elif self.__is_ether_bond and (not other.is_ether_bond()):
            return True
        else:
            if self.__C <= other.length():
                return True
            elif self.__C > other.length():
                return False
            else:
                if self.__DB <= other.db_index():
                    return True
                elif self.__DB > other.db_index():
                    return False
                else:
                    myoh = 0 if self.__OH is None else self.__OH
                    otheroh = 0 if other.hydroxylations() is None else other.hydroxylations()
                    if myoh <= otheroh:
                        return True
                    elif myoh > otheroh:
                        return False

    def modified_fa(self, c, db, oh) -> FA:
        return FA(self.__C+c, self.__DB+db, self.__OH+oh, self.__modifications, self.__is_long_chain_base,
                  self.__is_ether_bond, self.__ether_type)

    def as_ether(self, ether_type: str) -> FA:
        return FA(self.__C, self.__DB, self.__OH, self.__modifications, self.__is_long_chain_base,
                  is_ether_bond=True, ether_type=ether_type)

    def as_not_ether(self) -> FA:
        return FA(self.__C, self.__DB, self.__OH, self.__modifications, self.__is_long_chain_base,
                  is_ether_bond=False)


class Lipid:

    __slots__ = ["__lipid_class", "__head_group", "__fa_spots", "__backbone", "__non_fa_modifications", "__ids",
                 "_is_molecular_species", "__sum_length", "__sum_dbs", "__sum_ohs", "__sum_fa_modifications",
                 "__fatty_acids", "__number_fas", "__has_long_chain_base", "__has_ether_bond",
                 "__ether_type", "__dataname", "__converted_to_mol_spec", "__category", "__div_factor"]

    def __init__(self, lipid_class: str,
                 head_group: str,
                 is_molecular_species: bool,
                 fa_spots: int,
                 backbone: str = "glycerol",
                 dataname: str = None,
                 non_fa_modifications: list = None,
                 ids: dict = None,
                 fatty_acids: List[FA] = None,
                 sum_length: int = None,
                 sum_dbs: int = None,
                 sum_ohs: int = None,
                 sum_fa_modifications: list = None,
                 number_fas: int = None,
                 has_long_chain_base: int = None,
                 has_ether_bond: int = None,
                 ether_type: str = None,
                 converted_to_mol_spec: bool = False,
                 category: str = "Glycerolipids"):
        """
        Lipid class. Stores all necessary attributes of a lipid. Can be used to apply reaction rules to it.
        :param lipid_class: String, class of a lipid
        :param head_group: String, head group of a lipid
        :param is_molecular_species: Bool
        :param fa_spots: Int Number of possible fatty acids connected to this lipid
        :param backbone: String, Default="glycerol" backbone of the lipid (Important for reaction rules)
        :param non_fa_modifications: List of strings, Modification of the lipid (not related to faty acids)
        :param ids: dict, Database IDs of the lipid, with database as key and value as ID
        :param fatty_acids: list of fatty acids (class FA), required if is_molecular_species==True
        :param sum_length: Int, Number of carbons of the lipids, required if is_molecular_species==False
        :param sum_dbs: Int, Number of double bonds, required if is_molecular_species==False
        :param sum_ohs: Int, Number of hydroxylations of fatty acids, required if is_molecular_species==False, can be None
        :param sum_fa_modifications: List of strings, Modifications of fatty acids, required if is_molecular_species==False
        :param number_fas: Int, number of fatty acids attached to this lipid, required if is_molecular_species==False
        :param has_long_chain_base: Int, Number of long chain bases in this lipid, required if is_molecular_species==False
        """
        self.__lipid_class = lipid_class
        self.__head_group = head_group
        self.__fa_spots = fa_spots
        self.__backbone = backbone
        self.__category = category
        self.__non_fa_modifications = non_fa_modifications
        self.__ids = ids
        self._is_molecular_species = is_molecular_species
        self.__sum_length = sum_length
        self.__sum_dbs = sum_dbs
        self.__sum_ohs = sum_ohs
        self.__sum_fa_modifications = sum_fa_modifications
        self.__fatty_acids = fatty_acids
        self.__number_fas = number_fas
        self.__has_long_chain_base = has_long_chain_base
        self.__has_ether_bond = has_ether_bond
        self.__dataname = dataname
        self.__converted_to_mol_spec = converted_to_mol_spec
        if self.__has_ether_bond and (ether_type is None or ether_type==""):
            self.__ether_type = "O-"
        else:
            self.__ether_type = ether_type

        if is_molecular_species:
            if fatty_acids is None:
                raise AttributeError("if is_molecular_species==True, "
                                     "a list of fatty acids (class FA) must be provided.")
            else:
                self.__sum_length = None
                self.__sum_dbs = None
                self.__sum_ohs = None
                self.__sum_fa_modifications = None
                self.__number_fas = len(fatty_acids)
                self.__has_long_chain_base = None
                self.__has_ether_bond = None
        else:
            if (sum_length is None) or (sum_dbs is None) or (sum_ohs is None) or \
                    (sum_fa_modifications is None) or (number_fas is None) or (has_long_chain_base is None) or \
                    (has_ether_bond is None):
                raise AttributeError("if is_molecular_species==False, a all other arguments must be provided.")
            else:
                self.__fatty_acids = None

    def get_dataname(self):
        return self.__dataname

    def set_dataname(self, name):
        self.__dataname = name

    def is_molecular_species(self) -> bool:
        return self._is_molecular_species

    def get_headgroup(self) -> str:
        return self.__head_group

    def get_lipid_class(self) -> str:
        return self.__lipid_class

    def sum_length(self) -> int:
        if self._is_molecular_species:
            return sum([x.length() for x in self.__fatty_acids])
        else:
            return self.__sum_length

    def sum_dbs(self) -> int:
        if self._is_molecular_species:
            return sum([x.db_index() for x in self.__fatty_acids])
        else:
            return self.__sum_dbs

    def sum_ohs(self) -> int:
        if self._is_molecular_species:
            return sum([x.hydroxylations() for x in self.__fatty_acids if x.hydroxylations() is not None])
        else:
            return self.__sum_ohs

    def get_non_fa_modifications(self) -> List:
        return self.__non_fa_modifications

    def get_number_fas(self) -> int:
        if self._is_molecular_species:
            return len(self.__fatty_acids)
        return self.__number_fas

    def get_fa_spots(self) -> int:
        return self.__fa_spots

    def get_fa_lengths(self) -> List[int]:
        if self._is_molecular_species:
            return [x.length() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species (get_fa_lengths)")
            return []

    def get_fa_dbs(self) -> List[int]:
        if self._is_molecular_species:
            return [x.db_index() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species (get_fa_dbs)")
            return []

    def get_fa_ohs(self) -> List[int]:
        if self._is_molecular_species:
            return [x.hydroxylations() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species (get_fa_ohs)")
            return []

    def get_modifications(self):
        if self._is_molecular_species:
            return [x.modifications() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species (get_modifications)")
            return self.__sum_fa_modifications

    def get_fas(self) -> List[FA]:
        if self._is_molecular_species:
            return self.__fatty_acids
        else:
            print("Lipid is not a molecular species (get_fas)")
            return []

    def get_backbone(self) -> str:
        return self.__backbone

    def get_category(self) -> str:
        return self.__category

    def get_ids(self) -> dict:
        return self.__ids

    def get_fa_long_chain_base(self) -> List[bool]:
        if self._is_molecular_species:
            if len(self.__fatty_acids) == 0:
                return []
            return [x.is_long_chain_base() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species")
            return []

    def get_number_long_chain_base(self) -> int:
        if self._is_molecular_species:
            if len(self.__fatty_acids) == 0:
                return 0
            return sum([x.is_long_chain_base() for x in self.__fatty_acids])
        else:
            return self.__has_long_chain_base

    def get_ether(self) -> int:
        if self._is_molecular_species:
            if len(self.__fatty_acids) == 0:
                return 0
            return sum([int(x.is_ether_bond()) for x in self.__fatty_acids])
        else:
            return self.__has_ether_bond

    def get_fa_ether(self) -> List[bool]:
        if self._is_molecular_species:
            if len(self.__fatty_acids) == 0:
                return []
            return [x.is_ether_bond() for x in self.__fatty_acids]
        else:
            print("Lipid is not a molecular species")
            return []

    def get_ether_type(self) -> str:
        if self._is_molecular_species:
            if len(self.__fatty_acids) == 0:
                return []
            tmp = [x.get_ether_type() for x in self.__fatty_acids if x.get_ether_type() not in [None, ""]]
            if len(tmp) == 0:
                return ""
            elif len(tmp) == 1:
                return tmp[0]
            else:
                return str(tmp)
        else:
            return self.__ether_type

    def get_molecular_species(self, fatty_acids: List[FA]) -> List[Lipid]:
        if not all([isinstance(x, FA) for x in fatty_acids]):
            raise TypeError("All elements in 'fatty_acids' must be of type FA.")
        if self._is_molecular_species:
            warnings.warn("Lipid is already a molecular species")

        combinations = list()
        if self.get_ether():
            new_fa = fatty_acids.copy() + [x.as_ether(self.get_ether_type()) for x in fatty_acids]
            combs = itertools.combinations_with_replacement(new_fa, self.get_number_fas())
        else:
            combs = itertools.combinations_with_replacement(fatty_acids, self.get_number_fas())

        for i in combs:
            tmp_l = Lipid(lipid_class=self.get_lipid_class(),
                          head_group=self.__head_group,
                          is_molecular_species=True,
                          fa_spots=self.__fa_spots,
                          dataname=self.__dataname,
                          non_fa_modifications=self.__non_fa_modifications,
                          ids=self.__ids,
                          backbone=self.__backbone,
                          fatty_acids=list(i),
                          converted_to_mol_spec=True,
                          category=self.__category)

            if molecular_equals_sum_species(tmp_l, self):
                combinations.append(tmp_l)

        if len(combinations) == 0:
            raise MolecularSpeciesError(f"No molecular species could be inferred for {self.sum_species_str()}.\n"
                                        f"Try to add more possible fatty acids | {self.sum_species_str()}")
        return combinations

    def __str__(self) -> str:
        if self.is_molecular_species():
            if " O-" in self.__lipid_class:
                clsstr = self.__lipid_class.replace(" O-", "")
                return f"{clsstr}({'_'.join([str(x) for x in sorted(self.__fatty_acids)])})"
            else:
                return f"{self.__lipid_class}({'_'.join([str(x) for x in sorted(self.__fatty_acids)])})"
        else:
            return self.sum_species_str()

    def sum_species_str(self) -> str:
        if self.get_ether() and " O-" in self.__lipid_class:
            clsstr = self.__lipid_class.replace(" O-", "")
            out_str = f"{clsstr}("
        else:
            out_str = f"{self.__lipid_class}("
        if self.get_ether():
            out_str += self.get_ether_type()
        # if self.get_number_long_chain_base():
        #     out_str += "d"
        out_str += f"{self.sum_length()}:{self.sum_dbs()}"
        if self.sum_ohs():
            if self.sum_ohs() > 1:
                out_str += f";O{self.sum_ohs()}"
            else:
                out_str += f";O"
        return out_str + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def converted_to_mol_spec(self) -> bool:
        return self.__converted_to_mol_spec

    def get_native_string(self) -> str:
        if self.converted_to_mol_spec():
            return self.sum_species_str()
        else:
            return self.__str__()

    def set_div_factor(self, fac: float):
        self.__div_factor = fac

    def get_div_factor(self):
        return self.__div_factor

def molecular_equals_sum_species(ms: Lipid, ss: Lipid) -> bool:
    if ms.is_molecular_species() and not ss.is_molecular_species():
        if ms.get_ether() or ss.get_ether():
            return (ms.get_lipid_class() == ss.get_lipid_class()) and \
                   (ms.sum_length() == ss.sum_length()) and \
                   (ms.sum_dbs() == ss.sum_dbs()) and \
                   (ms.sum_ohs() == ss.sum_ohs()) and \
                   (ms.get_headgroup() == ss.get_headgroup()) and \
                   (ms.get_fa_spots() == ss.get_fa_spots()) and \
                   (ms.get_number_fas() == ss.get_number_fas()) and \
                   (ms.get_ether() == ss.get_ether()) and \
                   (ms.get_number_long_chain_base() == ms.get_number_long_chain_base()) and \
                   (ms.get_ether_type() == ss.get_ether_type())
        else:
            return (ms.get_lipid_class() == ss.get_lipid_class()) and \
                   (ms.sum_length() == ss.sum_length()) and \
                   (ms.sum_dbs() == ss.sum_dbs()) and \
                   (ms.sum_ohs() == ss.sum_ohs()) and \
                   (ms.get_headgroup() == ss.get_headgroup()) and \
                   (ms.get_fa_spots() == ss.get_fa_spots()) and \
                   (ms.get_number_fas() == ss.get_number_fas()) and \
                   (ms.get_ether() == ss.get_ether()) and \
                   (ms.get_number_long_chain_base() == ms.get_number_long_chain_base())
    else:
        warnings.warn("Comparison requires a molecular and a sum species lipid.")
        return False

if __name__ == "__main__":
    fa1 = FA(20, 4, None)
    fa2 = FA(18, 0, 0)
    fa3 = FA(22, 4, 0, is_ether_bond=True, ether_type="P-")
    lcb1 = FA(18, 0, 1, is_long_chain_base=True)

    pe1 = Lipid("PE", "PE", is_molecular_species=True, fa_spots=2, fatty_acids=[fa1, fa2])
    pe2 = Lipid("PE-O", "PE", is_molecular_species=True, fa_spots=2, fatty_acids=[fa1, fa3])
    sm1 = Lipid("SM", "PC", is_molecular_species=True, fa_spots=2, fatty_acids=[fa1, lcb1])

    print("++ Example molecular species++")
    print(pe1)
    print(pe2)
    print(sm1)

    pc1 = Lipid("PC", "PC", is_molecular_species=False, fa_spots=2, sum_length=34, sum_dbs=1, sum_ohs=0,
                sum_fa_modifications=[], number_fas=2, has_long_chain_base=0, has_ether_bond=0)

    print("")
    print("++ Example non molecular species++")
    print(pc1)

    print("")
    print("FA comparisson")
    print("FA(20, 4, 0) == FA(20, 4, 0): ", FA(20, 4, 0) == FA(20, 4, 0))
    print("FA(18, 1, 0) == FA(20, 4, 0): ", FA(18, 1, 0) == FA(20, 4, 0))

    # print(pc1.get_combinations_of_molecular_species([fa1, fa2, lcb1]))
