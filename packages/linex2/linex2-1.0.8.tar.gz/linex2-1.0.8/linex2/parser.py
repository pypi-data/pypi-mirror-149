from .reaction import FAReaction
from .lipid import FA, Lipid
from .exceptions import ParsingError, ReferenceLipidError
from .reference import ReferenceLipid
from typing import List, Dict, Tuple, Union
from numpy import ndarray
import os
import warnings
import re

# NOTE: for some reason LipidLynxX changes the
# working directory in ALL of these three cases:
# 1. module import
# 2. Converter object initialisation
# 3. Converter function calls
wdir = os.getcwd()
try:
    from lynx import Converter

    lynx_not_available: bool = False
except ModuleNotFoundError:
    print("Package 'lynx' (LipidLynxX) not available. Lipid name conversions will not be possible.")
    lynx_not_available: bool = True
os.chdir(wdir)


def parse_fa_reactions(lines: List[str]) -> List[FAReaction]:
    start = False
    list_of_reactions = []
    for line in lines:
        if start and (line[0] == ">"):
            start = False
        # Parsing of reactions
        # Hashtags are comments
        if start and line[0] != "#":
            fs = line.strip().split(",")
            if len(fs) > 1:
                c = 0
                db = 0
                oh = 0
                ether = False
                lcb = False
                r_name = ""
                for param in fs:
                    if len(param.strip().split(":")) == 3:
                        r_name = param.strip().split(":", maxsplit=1)[0]
                        param = param.strip().split(":", maxsplit=1)[1]
                    if param.strip()[:2] == "C:":
                        c = int(param.split(":")[1].strip())
                    if param.strip()[:2] == "DB":
                        db = int(param.split(":")[1].strip())
                    if param.strip()[:2] == "OH":
                        oh = int(param.split(":")[1].strip())
                    if param.strip() == "ether":
                        ether = True
                    if param.strip() == "lcb":
                        lcb = True
                if c != 0 or db != 0 or oh != 0:
                    list_of_reactions.append(FAReaction(c, db, oh,
                                                        valid_for_ether=ether,
                                                        valid_for_lcb=lcb,
                                                        name=r_name))

        if line.strip() == ">Reactions":
            start = True
    return list_of_reactions


def fa_parser(fa: str) -> FA:
    # required params
    oh = 0
    lcb = False
    ether = False
    ether_type = ""
    if "_" in fa or "/" in fa:
        raise ParsingError(f"Error in Fatty acid file: Could not parse fatty acid: {fa}")
    if "d" in fa or "D" in fa:
        fa = fa.replace("d", "")
        fa = fa.replace("D", "")
        if ";" in fa:
            if fa[-1] == "O":
                fa = fa + "3"
            else:
                fa = fa[0:-1] + str(int(fa[-1]) + 2)
        else:
            fa = fa + ";O2"
    try:
        fs = fa.split(":")
        first = fs[0]
        second = fs[1]

        # Front
        if first[0] == "l":
            lcb = True
            c = int(first[1:])
        elif first[:2].upper() in ["P-", "O-"]:
            ether = True
            ether_type = first[:2].upper()
            c = int(first[2:])
        else:
            c = int(first)

        # Remove
        if "(" in second:
            if "Z" in second:
                second = re.sub(r"\(.*\)", "", second)
            if "OH" in second:
                second = re.sub(r"\(.*\)", "", second)
                oh += 1
        # Back
        if ";" in second:
            db = int(second.split(";")[0])
            oh_dummy = second.split(";")[1]
            if oh_dummy == "O":
                oh += 1
            elif "O" in oh_dummy:
                oh += int(oh_dummy[1:])
            else:
                oh += int(oh_dummy)
        else:
            db = int(second)
    except:
        raise ParsingError(f"Error in Fatty acid file: Could not parse fatty acid: {fa}")

    return FA(c, db, oh=oh, is_long_chain_base=lcb, is_ether_bond=ether, ether_type=ether_type, modifications=[])


def parse_excluded_fa_reactions(lines: List[str]) -> List[List[FA]]:
    start = False
    list_of_reactions = []
    for line in lines:
        if start and (line[0] == ">"):
            start = False
        # Parsing of reactions
        # Hashtags are comments
        if start and line[0] != "#" and len(line.strip()) > 0:
            fs = line.strip().split(",")
            if len(fs) == 2:
                try:
                    list_of_reactions.append([fa_parser(fs[0].strip()), fa_parser(fs[1].strip())])
                except ParsingError:
                    ParsingError(f"Error in Fatty acid file: Could not read excluded reaction: {line.strip()}")
            else:
                print(f"Excluded reaction must be a list of two fatty acids. Ignoring line: {line.strip()}")
        if line.strip() == ">Excluded Reactions":
            start = True
    return list_of_reactions


def parse_fatty_acids(lines: List[str]) -> Dict[str, List[FA]]:
    start = False
    class_parser = False
    class_dict = {}
    list_of_curr_classes = []
    for line in lines:
        if start and (line[0] == ">"):
            start = False

        if line.strip()[0:8] == "Classes:":
            class_parser = True
            tmp_l = line.strip().split(":")[1]
            if len(tmp_l) == 0:
                list_of_curr_classes = ["all"]
                class_dict["all"] = []
            else:
                splits = tmp_l.split(",")
                splits = [x.strip() for x in splits]
                for a in splits:
                    class_dict[a] = []
                list_of_curr_classes = splits

        if start and line[0] != "#" and len(line.strip()) > 0 and not class_parser:
            fs = line.strip()
            if len(list_of_curr_classes) == 0:
                raise ParsingError("Error in Fatty acid file: No Classes defined for fatty acids")
            try:
                for a in list_of_curr_classes:
                    class_dict[a].append(fa_parser(fs))
            except ParsingError:
                ParsingError(f"Error in Fatty acid file: Could not read excluded fatty acid: {fs}")

        if line.strip() == ">Fatty Acids":
            start = True

        class_parser = False

    return class_dict


def save_lipidlynxx_converter(lipidname: str) -> str:
    if lynx_not_available:
        return lipidname
    try:
        orgwd = os.getcwd()
        conv = Converter()
        os.chdir(orgwd)
        outstr = conv.convert(lipidname.replace("_", "/")).dict()['output']
        os.chdir(orgwd)
        if outstr == '':
            return lipidname
        else:
            return outstr
    except:
        return lipidname


def lipid_parser(lipidname: str,
                 reference_lipids: Dict[str, ReferenceLipid],
                 is_ll_compatible: bool = False, org_name: str = "") -> Lipid:
    lipidname_new = lipidname.replace("_", "/")
    if is_ll_compatible:
        ln = lipidname_new.upper()
    else:
        ln = save_lipidlynxx_converter(lipidname_new.strip()).upper()
    # Get Lipid class
    firstsplit = ln.split("(", maxsplit=1)  # Prevent splitting hydroxilation or DB positions for single fatty acids
    lclass = firstsplit[0]

    if len(firstsplit) == 1:  # e.g. Cholesterol
        if not lclass in reference_lipids.keys():
            raise ReferenceLipidError(f"No compatiable lipid reference class found for Lipid: {lipidname}")
        ref_cls = reference_lipids[lclass]  # Matching reference to lipid

        lip = Lipid(ref_cls.get_abbr(),
                    ref_cls.get_headgroup(),
                    is_molecular_species=True,
                    fa_spots=ref_cls.get_potentialfas(),
                    dataname=org_name,
                    fatty_acids=[],
                    backbone=ref_cls.get_backbone(),
                    category=ref_cls.get_category())

        if ref_cls.is_of_class(lip):
            return lip
        else:
            raise ReferenceLipidError(
                f"Lipid: {lipidname} not compatible with reference class for {ref_cls.get_abbr()}.")

    farest = firstsplit[1]

    if lclass in reference_lipids.keys():
        if reference_lipids[lclass].get_ether():
            lclass = reference_lipids[lclass].get_abbr()
            if lclass[-1] == "P":
                farest = "P-" + farest
            if lclass[-1] == "O":
                farest = "O-" + farest
    # Check potential ethers
    # * Not i lclass
    if ("P-" not in lclass or "O-" not in lclass) and ("P-" in farest.upper() or "O-" in farest.upper()):
        lclass = lclass + " O-"
    # * P- in lclass
    elif ("P-" in lclass) and ("P-" not in farest.upper()):
        farest = "P-" + farest
        lclass = lclass.replace("P-", "O-")
    # * Not in farest
    elif ("O-" in lclass) and ("O-" not in farest.upper() or "P-" not in farest.upper()):
        farest = "O-" + farest
    # Check Class in Reference
    if not lclass in reference_lipids.keys():
        raise ReferenceLipidError(f"No compatiable lipid reference class found for Lipid: {lipidname}")
    ref_cls = reference_lipids[lclass]  # Matching reference to lipid
    # Recognize if SS or MS
    fas = farest[:-1].split("/")
    if len(fas) == ref_cls.get_fas():  # Molecular species
        if ref_cls.get_lcb():  # Currently only works with one ether and one LCB
            fas[0] = "l" + fas[0]
        lip = Lipid(lipid_class=ref_cls.get_abbr(),
                    head_group=ref_cls.get_headgroup(),
                    is_molecular_species=True,
                    fa_spots=ref_cls.get_potentialfas(),
                    dataname=org_name,
                    fatty_acids=[fa_parser(x) for x in fas],
                    backbone=ref_cls.get_backbone(),
                    category=ref_cls.get_category())
        if not ref_cls.is_of_class(lip):
            raise ReferenceLipidError(
                f"Lipid: {lipidname} not compatible with reference class for {ref_cls.get_abbr()}.")
        else:
            return lip
    elif len(fas) == 1:  # Sum species TODO: CL with 2 sum species
        sumfa = fa_parser(fas[0])
        lip = Lipid(lipid_class=ref_cls.get_abbr(),
                    head_group=ref_cls.get_headgroup(),
                    is_molecular_species=False,
                    fa_spots=ref_cls.get_potentialfas(),
                    dataname=org_name,
                    sum_length=sumfa.length(),  #
                    sum_dbs=sumfa.db_index(),  #
                    sum_ohs=sumfa.hydroxylations(),  #
                    sum_fa_modifications=sumfa.modifications(),
                    number_fas=ref_cls.get_fas(),
                    has_long_chain_base=ref_cls.get_lcb(),
                    has_ether_bond=ref_cls.get_ether(),
                    ether_type=sumfa.get_ether_type(),
                    backbone=ref_cls.get_backbone(),
                    category=ref_cls.get_category())
        if not ref_cls.is_of_class(lip):
            raise ReferenceLipidError(
                f"Lipid: {org_name} not compatible with reference class for {ref_cls.get_abbr()}.")
        else:
            return lip

    else:
        raise ReferenceLipidError(f"Number of fatty acids of lipid :{lipidname} not compatible with reference class.\n"
                                  f"The lipid can either be a sum species or have {ref_cls.get_fas()} fatty acids "
                                  f"as a molecular species.")


def parse_lipid_list(lipid_input: Union[List[str], ndarray],
                     reference_lipids: Dict[str, ReferenceLipid],
                     ll_compatible: bool = False) -> Tuple[Dict[str, List[Lipid]], Dict[str, str], List[str]]:
    # Return order: lipid_dict, converted_names_mapping (org_name -> converted_name), incompatible_lipids
    converted_names_mapping = {}
    incompatible_lipids = []
    lipid_dict = {}

    for org_name in lipid_input:
        if ll_compatible:
            conv_name = org_name
        else:
            conv_name = save_lipidlynxx_converter(org_name)

        try:
            tmp_lipid = lipid_parser(conv_name,
                                     reference_lipids=reference_lipids,
                                     is_ll_compatible=True,
                                     org_name=conv_name)
        except ReferenceLipidError as e:
            incompatible_lipids.append(org_name)
            warnings.warn(f"No compatible lipid class available. Error message: '{str(e)}'")
        except ParsingError as e:
            incompatible_lipids.append(org_name)
            warnings.warn(f"Error in parsing fatty acid. Error message: '{str(e)}'")
        else:  # If parsing was successful
            converted_names_mapping[org_name] = conv_name
            if tmp_lipid.get_lipid_class() in lipid_dict:
                lipid_dict[tmp_lipid.get_lipid_class()].append(tmp_lipid)
            else:
                lipid_dict[tmp_lipid.get_lipid_class()] = [tmp_lipid]

    return lipid_dict, converted_names_mapping, incompatible_lipids
