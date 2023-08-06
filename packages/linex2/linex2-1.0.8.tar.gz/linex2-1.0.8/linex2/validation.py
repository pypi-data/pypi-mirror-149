from .reference import ReferenceLipid
from typing import List
import warnings

from . import reaction_types

__reaction_types__ = [x for x in dir(reaction_types) if not x.startswith("_")]


def reaction_validator(reaction_type: str, substrates: List[ReferenceLipid], products: List[ReferenceLipid],
                       verbose=True) -> bool:

    if (reaction_type is None) or (reaction_type == "") or (reaction_type not in __reaction_types__):
        raise KeyError("reaction type not (correctly) specified")

    # No lipid on on or both sides
    if (len(substrates) == 0) or (len(products) == 0):
        if verbose:
            warnings.warn("Boundary reaction. Lipids on at least one site missing.")
            print("Boundary reaction. Lipids on at least one site missing.")
        return True

    # One lipid on each side
    elif (len(substrates) == 1) and (len(products) == 1):
        if reaction_type == "L_HGmodify":
            return (substrates[0].get_fas() == products[0].get_fas()) \
                   and (substrates[0].get_ether() == products[0].get_ether()) \
                   and (substrates[0].get_lcb() == products[0].get_lcb()) \
                   and (substrates[0].get_potentialfas() == products[0].get_potentialfas()) \
                   and (substrates[0].get_headgroup() != products[0].get_headgroup())

        elif reaction_type == "L_HGdelete":
            return (substrates[0].get_fas() == products[0].get_fas()) \
                   and (substrates[0].get_ether() == products[0].get_ether()) \
                   and (substrates[0].get_lcb() == products[0].get_lcb()) \
                   and (((substrates[0].get_headgroup() != "") and (products[0].get_headgroup() == ""))
                        or ((substrates[0].get_headgroup() == "") and (products[0].get_headgroup() != "")))

        elif reaction_type == "L_FAdelete":
            return (substrates[0].get_ether() == products[0].get_ether()) \
                   and (substrates[0].get_lcb() == products[0].get_lcb()) \
                   and (substrates[0].get_potentialfas() == products[0].get_potentialfas()) \
                   and (substrates[0].get_headgroup() == products[0].get_headgroup()) \
                   and (((substrates[0].get_fas()+1) == products[0].get_fas())
                        or (substrates[0].get_fas() == (products[0].get_fas()+1)))

        elif reaction_type == "L_merge":
            if verbose:
                warnings.warn("Reaction with one product and one substrate defined as 'L_merge'")
                print("Reaction with one product and one substrate defined as 'L_merge'")
            return False

        elif reaction_type == "L_FAether":
            return (((substrates[0].get_ether()-1) == products[0].get_ether())
                    or (substrates[0].get_ether() == (products[0].get_ether()))-1) \
                   and (substrates[0].get_lcb() == products[0].get_lcb()) \
                   and (substrates[0].get_potentialfas() == products[0].get_potentialfas()) \
                   and (substrates[0].get_headgroup() == products[0].get_headgroup()) \
                   and ((substrates[0].get_fas()) == products[0].get_fas())
        else:
            if verbose:
                warnings.warn("Reaction " + reaction_type +
                              " not implemented for a reaction with one substrate and one product.")
                print("Reaction " + reaction_type +
                      " not implemented for a reaction with one substrate and one product.")
            return False

    # 2&1 or 1&2
    elif ((len(substrates) == 1) and (len(products) == 2)) or ((len(substrates) == 2) and (len(products) == 1)):
        twos = substrates if len(substrates) == 2 else products
        ones = substrates if len(substrates) == 1 else products

        if reaction_type == "L_FAdelete":
            return (ones[0].get_fas() == sum([x.get_fas() for x in twos])) \
                   and any([x.get_headgroup() == ones[0].get_headgroup() for x in twos]) \
                   and any([x.get_potentialfas() > x.get_fas() for x in twos])

        elif reaction_type == "L_HGdelete":
            return (ones[0].get_fas() == sum([x.get_fas() for x in twos])) \
                   and any([x.get_headgroup() == ones[0].get_headgroup() for x in twos])

        elif reaction_type == "L_merge":
            return ones[0].get_fas() == sum([x.get_fas() for x in twos])  # TODO: Check LCB and Ether

        else:
            if verbose:
                warnings.warn(reaction_type + " not implemented for (1,2) or (2,1) reactions")
                print(reaction_type + " not implemented for (1,2) or (2,1) reactions")
            return False

    # 2&2
    elif (len(substrates) == 2) and (len(products) == 2):
        if reaction_type == "L_FAdelete":
            return (sum([x.get_fas() for x in substrates]) == sum([x.get_fas() for x in products])) \
                   and (all([x.get_headgroup() in [y.get_headgroup() for y in products] for x in substrates]))

        elif reaction_type in ["L_HGdelete", "L_HGmodify"]:
            return (sum([x.get_fas() for x in substrates]) == sum([x.get_fas() for x in products])) \
                   and (all([x.get_fas() in [y.get_fas() for y in products] for x in substrates]))

        else:
            if verbose:
                warnings.warn(reaction_type + " not implemented for (2,2) reactions")
                print(reaction_type + " not implemented for (2,2) reactions")
            return False

    else:
        raise NotImplementedError(reaction_type + " with " + str([len(substrates), len(products)]) + ", but the only possible combinations of substrate product pairs are currently "
                                  "(0,1);(1,0);(1,1);(1,2);(2,1);(2,2)")
