import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from .reference import ReferenceLipid
from .reaction import Reaction, FAReaction
from .reaction_types import *
from .lipid import Lipid
from .edgelist import Edge, Edgelist
import warnings


def make_organism_reaction_list_from_reactome(molecules: pd.DataFrame,
                                              curated_reactions: pd.DataFrame,
                                              reaction_to_molecules: pd.DataFrame,
                                              ref_lips: Dict[str, ReferenceLipid],
                                              reaction_details: pd.DataFrame,
                                              verbose: bool = True,
                                              organism: str = "HSA") -> List[Reaction]:
    n_reactions = curated_reactions.shape[0]
    merged_reaction_ids = curated_reactions["reaction_IDs"]
    reaction_type = curated_reactions["reaction_type"]
    reaction_notes = curated_reactions["reaction_notes"]
    reaction_details = reaction_details.drop_duplicates().set_index("EnzymeID")
    out_l = []

    organism = organism.upper()

    for r in range(n_reactions):

        subs = []
        prods = []
        if (organism in merged_reaction_ids[r]) and (reaction_type[r] is not np.nan):
            id_l = merged_reaction_ids[r].split(";")

            # Takes only one ID, because we expect the same reaction participants for the same reactions
            tmp_hsa = [x for x in id_l if organism in x]
            hsa_id = tmp_hsa[0]
            hsa_ids = ";".join(tmp_hsa)

            curr_rtm = reaction_to_molecules[reaction_to_molecules["ReactionID"] == hsa_id]
            n_curr_rtm = curr_rtm.shape[0]
            # Non-lipid participants in reactions
            nl_p = []
            for sp in range(n_curr_rtm):
                curr_mol = curr_rtm["MoleculeID"].values[sp]
                curr_part = curr_rtm["Participation"].values[sp]
                curr_st = curr_rtm["Stiochiometry"].values[sp]

                curr_other = molecules[molecules["ID"] == curr_mol]
                if curr_other.shape[0] != 0:
                    if curr_other["Abbreviation"].values[0] is not np.nan:
                        if curr_other["Abbreviation"].values[0].upper() in ref_lips.keys():
                            if curr_part == "Substrate":
                                subs += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                            else:
                                prods += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                        else:
                            nl_p.append(curr_other["name1"].values[0])
                    else:
                        nl_p.append(curr_other["name1"].values[0])

            if len(subs) > 0 or len(prods) > 0:
                if hsa_id in reaction_details.index:
                    tmp_id = reaction_details.loc[hsa_id, :]["UniProtID"]
                    if isinstance(tmp_id, pd.Series):
                        up_id = ", ".join([str(x) for x in tmp_id.values])
                    else:
                        up_id = str(tmp_id)
                    up_id = up_id if up_id != "nan" else ""

                    tmp_id = reaction_details.loc[hsa_id, :]["GeneName"]
                    if isinstance(tmp_id, pd.Series):
                        gn_id = ", ".join([str(x) for x in tmp_id.values])
                    else:
                        gn_id = str(tmp_id)
                    gn_id = gn_id if gn_id != "nan" else ""
                else:
                    up_id = ""
                    gn_id = ""
                new_reac = Reaction(substrates=subs,
                                    products=prods,
                                    reaction_type=reaction_type[r],
                                    enzyme_ids=hsa_ids,
                                    non_lipid_reaction_participants=nl_p,
                                    uniprot=up_id,
                                    gene_name=gn_id)
                if new_reac not in out_l:
                    if verbose:
                        a = [x.get_enzyme_repr() for x in out_l if new_reac.participation_equality(x)
                             and new_reac.get_reaction_type() != x.get_reaction_type()]
                        if len(a) > 0:
                            print("Reaction " + new_reac.get_enzyme_id() + " has the same participants as " + str(a) +
                                  " but different Reaction types.")
                    out_l.append(new_reac)

                else:
                    for tr in range(len(out_l)):
                        if new_reac == out_l[tr]:
                            out_l[tr].extend_enzyme_ids(hsa_ids)
                            if up_id != "":
                                out_l[tr].extend_uniprot(up_id)
                            if gn_id != "":
                                out_l[tr].extend_uniprot(gn_id)
                            out_l[tr].extend_nl_participants(nl_p)
                            break
        else:
            pass

    return out_l


def make_all_reaction_list_from_reactome(molecules: pd.DataFrame,
                                         curated_reactions: pd.DataFrame,
                                         reaction_to_molecules: pd.DataFrame,
                                         ref_lips: Dict[str, ReferenceLipid],
                                         reaction_details: pd.DataFrame,
                                         verbose: bool = True) -> Tuple[List[Reaction], int]:
    n_reactions = curated_reactions.shape[0]
    merged_reaction_ids = curated_reactions["reaction_IDs"]
    reaction_type = curated_reactions["reaction_type"]
    # reaction_notes = curated_reactions["reaction_notes"]
    reaction_details = reaction_details.drop_duplicates().set_index("EnzymeID")
    out_l = []
    conflict_counter = 0
    for r in range(n_reactions):

        if reaction_type[r] is not np.nan:
            id_l = merged_reaction_ids[r].split(";")

            for ids in id_l:
                hsa_id = ids
                subs = []
                prods = []
                curr_rtm = reaction_to_molecules[reaction_to_molecules["ReactionID"] == hsa_id]
                n_curr_rtm = curr_rtm.shape[0]
                nl_p = []
                for sp in range(n_curr_rtm):

                    curr_mol = curr_rtm["MoleculeID"].values[sp]
                    curr_part = curr_rtm["Participation"].values[sp]
                    curr_st = curr_rtm["Stiochiometry"].values[sp]

                    curr_other = molecules[molecules["ID"] == curr_mol]
                    if curr_other.shape[0] != 0:
                        if curr_other["Abbreviation"].values[0] is not np.nan:
                            if curr_other["Abbreviation"].values[0].upper() in ref_lips.keys():
                                if curr_part == "Substrate":
                                    subs += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                                else:
                                    prods += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                            else:
                                nl_p.append(curr_other["name1"].values[0])
                        else:
                            nl_p.append(curr_other["name1"].values[0])
                if len(subs) > 0 or len(prods) > 0:
                    if hsa_id in reaction_details.index:
                        tmp_id = reaction_details.loc[hsa_id, :]["UniProtID"]
                        if isinstance(tmp_id, pd.Series):
                            up_id = ", ".join([str(x) for x in tmp_id.values])
                        else:
                            up_id = str(tmp_id)
                        up_id = up_id if up_id != "nan" else ""

                        tmp_id = reaction_details.loc[hsa_id, :]["GeneName"]
                        if isinstance(tmp_id, pd.Series):
                            gn_id = ", ".join([str(x) for x in tmp_id.values])
                        else:
                            gn_id = str(tmp_id)
                        gn_id = gn_id if gn_id != "nan" else ""

                    else:
                        up_id = ""
                        gn_id = ""
                    new_reac = Reaction(substrates=subs,
                                        products=prods,
                                        reaction_type=reaction_type[r],
                                        enzyme_ids=hsa_id,
                                        non_lipid_reaction_participants=nl_p,
                                        uniprot=up_id,
                                        gene_name=gn_id)
                    if new_reac not in out_l:
                        a = [x.get_enzyme_repr() for x in out_l if new_reac.participation_equality(x)
                             and new_reac.get_reaction_type() != x.get_reaction_type()]
                        if len(a) > 0:
                            l_str = str(a)
                            conflict_counter += 1
                            if verbose:
                                if len(l_str) > 30:
                                    print("Reaction " + new_reac.get_enzyme_id() + " has the same participants as " +
                                          l_str[0:30] + "...] but different Reaction types.\n")
                                else:
                                    print("Reaction " + new_reac.get_enzyme_id() + " has the same participants as " +
                                          l_str + " but different Reaction types.\n")
                        out_l.append(new_reac)

                    else:
                        for tr in range(len(out_l)):
                            if new_reac == out_l[tr]:
                                out_l[tr].extend_enzyme_ids(hsa_id)
                                if up_id != "":
                                    out_l[tr].extend_uniprot(up_id)
                                if gn_id != "":
                                    out_l[tr].extend_uniprot(gn_id)
                                out_l[tr].extend_nl_participants(nl_p)
                                break

        else:
            pass

    return out_l, conflict_counter


def make_all_reaction_list_from_rhea(molecules: pd.DataFrame,
                                     curated_reactions: pd.DataFrame,
                                     reaction_to_molecules: pd.DataFrame,
                                     ref_lips: Dict[str, ReferenceLipid],
                                     gn_mapping: pd.DataFrame,
                                     verbose=True) -> Tuple[List[Reaction], int]:
    n_reactions = curated_reactions.shape[0]
    merged_reaction_ids = curated_reactions["reaction_IDs"]
    reaction_type = curated_reactions["reaction_type"]
    # reaction_notes = curated_reactions["reaction_notes"]

    out_l = []
    conflict_counter = 0
    for r in range(n_reactions):

        if reaction_type[r] is not np.nan:
            id_l = merged_reaction_ids[r].split(";")

            for ids in id_l:
                hsa_id = ids
                subs = []
                prods = []
                curr_rtm = reaction_to_molecules[reaction_to_molecules["ReactionID"] == hsa_id]
                n_curr_rtm = curr_rtm.shape[0]
                nl_p = []
                for sp in range(n_curr_rtm):

                    curr_mol = curr_rtm["MoleculeID"].values[sp]
                    curr_part = curr_rtm["Participation"].values[sp]
                    curr_st = curr_rtm["Stiochiometry"].values[sp]
                    curr_other = molecules[molecules["ChEBI"] == curr_mol]
                    if curr_other.shape[0] != 0:
                        if curr_other["Abbreviation"].values[0] is not np.nan:
                            if curr_other["Abbreviation"].values[0].upper() in ref_lips.keys():
                                if curr_part == "Substrate":
                                    subs += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                                else:
                                    prods += [ref_lips[curr_other["Abbreviation"].values[0].upper()]] * curr_st
                            else:
                                nl_p.append(curr_other["name1"].values[0])
                        else:
                            nl_p.append(curr_other["name1"].values[0])

                if len(subs) > 0 or len(prods) > 0:

                    if hsa_id in gn_mapping.index:
                        tmp_id = gn_mapping.loc[hsa_id, :]["ID"]
                        if isinstance(tmp_id, pd.Series):
                            up_id = ", ".join([str(x) for x in tmp_id.values])
                        else:
                            up_id = str(tmp_id)
                        up_id = up_id if up_id != "nan" else ""

                        tmp_id = gn_mapping.loc[hsa_id, :]["GeneName"]
                        if isinstance(tmp_id, pd.Series):
                            gn_id = ", ".join([str(x) for x in tmp_id.values])
                        else:
                            gn_id = str(tmp_id)
                        gn_id = gn_id if gn_id != "nan" else ""
                    else:
                        up_id = ""
                        gn_id = ""
                    new_reac = Reaction(substrates=subs,
                                        products=prods,
                                        reaction_type=reaction_type[r],
                                        enzyme_ids=hsa_id,
                                        non_lipid_reaction_participants=nl_p,
                                        uniprot=up_id,
                                        gene_name=gn_id)

                    if new_reac not in out_l:
                        a = [x.get_enzyme_id() for x in out_l if new_reac.participation_equality(x)
                             and new_reac.get_reaction_type() != x.get_reaction_type()]
                        if len(a) > 0:
                            l_str = str(a)
                            conflict_counter += 1
                            if verbose:
                                if len(l_str) > 30:
                                    print("Reaction " + new_reac.get_enzyme_id() + " has the same participants as " +
                                          l_str[0:30] + "...] but different Reaction types.\n")
                                else:
                                    print("Reaction " + new_reac.get_enzyme_id() + " has the same participants as " +
                                          l_str + " but different Reaction types.\n")
                        out_l.append(new_reac)

                    else:
                        for tr in range(len(out_l)):
                            if new_reac == out_l[tr]:
                                out_l[tr].extend_enzyme_ids(hsa_id)
                                if up_id != "":
                                    out_l[tr].extend_uniprot(up_id)
                                if gn_id != "":
                                    out_l[tr].extend_uniprot(gn_id)
                                out_l[tr].extend_nl_participants(nl_p)
                                break

        else:
            pass

    return out_l, conflict_counter


def extender(class_reactions: List[Reaction], fa_reactions: List[FAReaction],
             lip_dict: Dict[str, List[Lipid]]) -> Edgelist:
    warnings.warn("extender function in deprecated and will be removed soon. "
                  "Please switch to the Extender class or contact Tim.")
    edge_list = Edgelist()

    # Loop over class reactions
    for i in class_reactions:
        if i.is_valid(verbose=False):
            if i.shape() == (0, 1) or i.shape() == (1, 0):
                pass
            elif i.shape() == (1, 1):
                # Pick both classed from lip_dict
                sub_ref = i.get_substrates()[0]
                prod_ref = i.get_products()[0]
                if sub_ref.get_abbr() in lip_dict and prod_ref.get_abbr() in lip_dict:
                    pot_subs = lip_dict[sub_ref.get_abbr()]
                    pot_prods = lip_dict[prod_ref.get_abbr()]

                    if i.get_reaction_type() == L_HGmodify or i.get_reaction_type() == L_HGdelete:
                        # Loop over both of them
                        for l1 in pot_subs:
                            for l2 in pot_prods:
                                # get pairs
                                if sorted(l1.get_fas()) == sorted(l2.get_fas()):
                                    edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                            reaction_type=i.get_reaction_type(), notes=""))

                    elif i.get_reaction_type() == L_FAdelete:
                        # Loop over both of them
                        for l1 in pot_subs:
                            for l2 in pot_prods:
                                # get pairs
                                f1 = l1.get_fas()
                                f2 = l2.get_fas()

                                for ff1 in range(len(f1)):
                                    if sorted(f1) == sorted(f2+[f1[ff1]]):
                                        edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                                reaction_type=i.get_reaction_type(), notes=""))
                                        break
                                for ff2 in range(len(f2)):
                                    if sorted(f2) == sorted(f1+[f2[ff2]]):
                                        edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                                reaction_type=i.get_reaction_type(), notes=""))
                                        break

            elif i.shape() == (1, 2) or i.shape() == (2, 1):
                if i.get_reaction_type() == L_FAdelete:
                    twos = i.get_substrates() if len(i.get_substrates()) == 2 else i.get_products()
                    ones = i.get_substrates() if len(i.get_substrates()) == 1 else i.get_products()
                    one = ones[0]
                    t1 = twos[0]
                    t2 = twos[1]
                    # find partner
                    if one.get_headgroup() == t1.get_headgroup() and one.get_lcb() == t1.get_lcb() and \
                            one.get_ether() == t1.get_ether():
                        partner = t1
                        other = t2
                    else:
                        partner = t2
                        other = t1
                    if one.get_abbr() in lip_dict and partner.get_abbr() in lip_dict and other.get_abbr() in lip_dict:
                        one_pos = lip_dict[one.get_abbr()]
                        partner_pot = lip_dict[partner.get_abbr()]
                        other_pot = lip_dict[other.get_abbr()]
                        for l1 in one_pos:
                            for l2 in partner_pot:
                                for l3 in other_pot:
                                    for fa in l3.get_fas():
                                        if sorted(l1.get_fas()) == sorted(l2.get_fas() + [fa]):
                                            edge_list.add_edge(
                                                Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                     reaction_type=i.get_reaction_type(), notes=""))
                                            # TODO: Other lipid is skipped for now and not part of the edgelist!

                elif i.get_reaction_type() == L_merge:
                    twos = i.get_substrates() if len(i.get_substrates()) == 2 else i.get_products()
                    ones = i.get_substrates() if len(i.get_substrates()) == 1 else i.get_products()
                    one = ones[0]
                    t1 = twos[0]
                    t2 = twos[1]
                    if one.get_abbr() in lip_dict and t1.get_abbr() in lip_dict and t2.get_abbr() in lip_dict:
                        one_pos = lip_dict[one.get_abbr()]
                        partner_pot = lip_dict[t1.get_abbr()]
                        other_pot = lip_dict[t2.get_abbr()]

                        for l1 in one_pos:
                            for l2 in partner_pot:
                                for l3 in other_pot:
                                    if sorted(l1.get_fas()) == sorted(l2.get_fas() + l3.get_fas()):
                                        edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                                reaction_type=i.get_reaction_type(), notes=""))
                                        edge_list.add_edge(Edge(l1, l3, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                                reaction_type=i.get_reaction_type(), notes=""))

            elif i.shape() == (2, 2):
                subs = i.get_substrates()
                prods = i.get_products()
                if i.get_reaction_type() == L_FAdelete:
                    if subs[0].get_headgroup() == prods[0].get_headgroup() and \
                       subs[0].get_lcb() == prods[0].get_lcb() and \
                       subs[0].get_ether() == prods[0].get_ether() and \
                       subs[0].get_potentialfas() == prods[0].get_potentialfas():
                        p11 = subs[0]
                        p12 = prods[0]
                        p21 = subs[1]
                        p22 = prods[1]
                    else:
                        p11 = subs[0]
                        p12 = prods[1]
                        p21 = subs[1]
                        p22 = prods[0]

                    if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and p21.get_abbr() in lip_dict and \
                            p22.get_abbr() in lip_dict:
                        for l1 in lip_dict[p11.get_abbr()]:
                            for l2 in lip_dict[p12.get_abbr()]:
                                for l3 in lip_dict[p21.get_abbr()]:
                                    for l4 in lip_dict[p22.get_abbr()]:
                                        fa_set = set(l1.get_fas() + l2.get_fas() + l3.get_fas() + l4.get_fas())
                                        for fa in fa_set:
                                            if (sorted(l1.get_fas()) == sorted(l2.get_fas() + [fa]) or
                                               sorted(l1.get_fas() + [fa]) == sorted(l2.get_fas())) and \
                                               (sorted(l3.get_fas()) == sorted(l4.get_fas() + [fa]) or
                                               sorted(l3.get_fas() + [fa]) == sorted(l4.get_fas())):
                                                edge_list.add_edge(
                                                    Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                         reaction_type=i.get_reaction_type(), notes=""))
                                                edge_list.add_edge(
                                                    Edge(l3, l4, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                         reaction_type=i.get_reaction_type(), notes=""))

                elif i.get_reaction_type() == L_HGdelete or i.get_reaction_type() == L_HGmodify:
                    if subs[0].get_headgroup() == prods[0].get_headgroup() and \
                            subs[0].get_lcb() == prods[1].get_lcb() and subs[0].get_ether() == prods[1].get_ether():
                        p11 = subs[0]
                        p12 = prods[1]
                        p21 = subs[1]
                        p22 = prods[0]
                    else:
                        p11 = subs[0]
                        p12 = prods[0]
                        p21 = subs[1]
                        p22 = prods[1]
                    if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and p21.get_abbr() in lip_dict and \
                            p22.get_abbr() in lip_dict:
                        for l1 in lip_dict[p11.get_abbr()]:
                            for l2 in lip_dict[p12.get_abbr()]:
                                for l3 in lip_dict[p21.get_abbr()]:
                                    for l4 in lip_dict[p22.get_abbr()]:
                                        if sorted(l1.get_fas()) == sorted(l2.get_fas()) and \
                                                sorted(l3.get_fas()) == sorted(l4.get_fas()):
                                            edge_list.add_edge(
                                                Edge(l1, l2, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                     reaction_type=i.get_reaction_type(), notes=""))
                                            edge_list.add_edge(
                                                Edge(l3, l4, enzyme_id=i.get_enzyme_repr(), reaction_id="r_id",
                                                     reaction_type=i.get_reaction_type(), notes=""))

    # Fatty Acid reactions
    for far in fa_reactions:
        # loop over lipids -> FA modifications are only possible for lipids of one class
        for lip in lip_dict:
            if len(lip_dict[lip]) > 1:
                for l1 in lip_dict[lip]:
                    for l2 in lip_dict[lip]:
                        if far.is_transformable(l1, l2):
                            edge_list.add_edge(Edge(l1, l2, enzyme_id="", reaction_id="r_id",
                                                    reaction_type="L_FAmodify", notes=far.get_last_conversion()))

    return edge_list

