from typing import List, Dict
from .reaction import Reaction, FAReaction
from .lipid import Lipid, FA
from .edgelist import Edge, Edgelist
from .reaction_types import *
from .reference import ReferenceLipid
from multiprocessing import Process, Queue
from datetime import datetime
import itertools

class Extender:

    __slots__ = ["__class_reacs", "__fa_reacs"]

    def __init__(self, class_reactions: List[Reaction], fatty_acid_reactions: List[FAReaction]):
        self.__class_reacs = class_reactions
        self.__fa_reacs = fatty_acid_reactions

    def evaluate_fa_reactions(self, lip_dict: Dict[str, List[Lipid]],
                              excluded_fa_conversions: List[List[FA]] = None, startid=0) -> Edgelist:

        return evaluate_fa_reactions_static(lip_dict, self.__fa_reacs, excluded_fa_conversions, startid=startid)

    def evaluate_fa_reactions_parallel(self, lip_dict: Dict[str, List[Lipid]], n_processes: int,
                              excluded_fa_conversions: List[List[FA]] = None) -> Edgelist:
        queue = Queue()
        split = len(self.__class_reacs) // n_processes
        p = [Process(target=evaluate_fa_reactions_worker,
                     args=(queue, lip_dict, self.__fa_reacs[(split * x):(split * (x + 1))], excluded_fa_conversions)) for x in
             range(n_processes - 1)]
        p.append(Process(target=evaluate_fa_reactions_worker,
                         args=(queue, lip_dict, self.__fa_reacs[(split * (n_processes - 1)):], excluded_fa_conversions)))

        for pi in p:
            pi.start()
        results = [queue.get() for pr in range(n_processes)]
        for pj in p:
            pj.join()

        a = Edgelist()
        for r in results:
            a = a + r

        return a

    def evaluate_class_reactions(self, lip_dict: Dict[str, List[Lipid]], startid: int =0) -> Edgelist:
        return evaluate_class_reactions_static(self.__class_reacs, lip_dict, startid=startid)

    def evaluate_ether_conversions(self, lip_dict: Dict[str, List[Lipid]],
                                   reference_lipids: List[ReferenceLipid], startid: int =0) -> Edgelist:
        return evaluate_ether_conversions_static(lip_dict, reference_lipids=reference_lipids, startid=startid)

    def evaluate_class_reactions_parallel(self, lip_dict: Dict[str, List[Lipid]], n_processes: int) -> Edgelist:
        queue = Queue()
        split = len(self.__class_reacs) // n_processes
        p = [Process(target=evaluate_class_reactions_worker,
                     args=(queue, self.__class_reacs[(split*x):(split*(x+1))], lip_dict)) for x in range(n_processes-1)]
        p.append(Process(target=evaluate_class_reactions_worker,
                         args=(queue, self.__class_reacs[(split*(n_processes-1)):], lip_dict)))
        # p1 = Process(target=evaluate_class_reactions_worker, args=(queue, self.__class_reacs[:split], lip_dict))
        # p2 = Process(target=evaluate_class_reactions_worker, args=(queue, self.__class_reacs[split:], lip_dict))
        # p1.start()
        # p2.start()
        for pi in p:
            pi.start()
        results = [queue.get() for pr in range(n_processes)]
        for pj in p:
            pj.join()

        a = Edgelist()
        for r in results:
            a = a + r

        return a

    def evaluate_all(self, lip_dict: Dict[str, List[Lipid]],
                     excluded_fa_conversions: List[List[FA]] = None,
                     ether_conversions: bool = False,
                     reference_lipids: List[ReferenceLipid] = None) -> Edgelist:
        # Class reactions
        tmp1 = self.evaluate_class_reactions(lip_dict)
        stid = tmp1.raw_edgelist_copy()[-1].get_reaction_id()
        # FA reactions
        tmp2 = self.evaluate_fa_reactions(lip_dict, excluded_fa_conversions, startid=int(stid)+1)
        tmp2_ed = tmp2.raw_edgelist_copy()
        if len(tmp2_ed) > 0:
            stid = tmp2.raw_edgelist_copy()[-1].get_reaction_id()
        # Ether conversions
        tmp3 = Edgelist()
        if ether_conversions:
            if reference_lipids is not None:
                tmp3 = self.evaluate_ether_conversions(lip_dict=lip_dict,
                                                       reference_lipids=reference_lipids,
                                                       startid=int(stid)+1)

        return tmp1 + tmp2 + tmp3

    def evaluate_all_parallel(self, lip_dict: Dict[str, List[Lipid]], n_processes: int,
                              excluded_fa_conversions: List[List[FA]] = None) -> Edgelist:
        tmp1 = self.evaluate_class_reactions(lip_dict)
        tmp2 = self.evaluate_fa_reactions_parallel(lip_dict, n_processes, excluded_fa_conversions)
        return tmp1 + tmp2

        return  tmp1 + tmp2


def lfad22_inner(i: Reaction, r1: List[Lipid], l1: Lipid, l2: Lipid, l3: Lipid, rid: int = 0) -> List[Edge]:
    for l4 in r1:
        fa_set = set(l1.get_fas() + l2.get_fas() + l3.get_fas() + l4.get_fas())
        for fa in fa_set:
            if (sorted(l1.get_fas()) == sorted(l2.get_fas() + [fa]) or
                sorted(l1.get_fas() + [fa]) == sorted(l2.get_fas())) and \
                    (sorted(l3.get_fas()) == sorted(l4.get_fas() + [fa]) or
                     sorted(l3.get_fas() + [fa]) == sorted(l4.get_fas())):

                return [Edge(l1, l2, enzyme_id=i.get_enzyme_id(), reaction_id=str(rid),
                             reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                             gene_name=i.get_gene_name(),
                             reaction_structure="2,2", l1_type="substrate", l2_type="product",
                             nl_participants=i.get_nl_participants()),
                        Edge(l3, l4, enzyme_id=i.get_enzyme_id(), reaction_id=str(rid),
                             reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                             gene_name=i.get_gene_name(),
                             reaction_structure="2,2", l1_type="substrate", l2_type="product",
                             nl_participants=i.get_nl_participants())]
    return []


def lhg22_inner(i: Reaction, r1: List[Lipid], l1: Lipid, l2: Lipid, l3: Lipid) -> List[Edge]:
    for l4 in r1:
        if sorted(l1.get_fas()) == sorted(l2.get_fas()) and \
                sorted(l3.get_fas()) == sorted(l4.get_fas()):
            return [Edge(l1, l2, enzyme_id=i.get_enzyme_id(), reaction_id="r_id",
                         reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                             gene_name=i.get_gene_name(),
                             nl_participants=i.get_nl_participants()),
                    Edge(l3, l4, enzyme_id=i.get_enzyme_id(), reaction_id="r_id",
                         reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                             gene_name=i.get_gene_name(),
                             nl_participants=i.get_nl_participants())]
    return []


def evaluate_class_reactions_static(class_reacs: List[Reaction],
                                    lip_dict: Dict[str, List[Lipid]], startid: int = 0) -> Edgelist:
    edge_list = Edgelist()

    # TODO: Function too big. Should be split up into multiple functions.

    # Loop over class reactions
    curr_reac_id = startid
    l_counter = 0
    for i in class_reacs:
        # print(f"reaction {l_counter} of {len(class_reacs)} ({str(i)})")
        # l_counter += 1

        if i.is_valid(verbose=False):
            if i.subs_eq_prods():
                continue
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
                                    edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                                                            reaction_id=str(curr_reac_id),
                                                            reaction_type=i.get_reaction_type(), notes="",
                                                            uniprot=i.get_uniprot(),
                                                            gene_name=i.get_gene_name(),
                                                            fa_param=str(l1.sum_length()),
                                                            nl_participants=i.get_nl_participants()))
                                    curr_reac_id += 1
                                    break
                    elif i.get_reaction_type() == L_FAdelete:
                        # Loop over both of them
                        for l1 in pot_subs:
                            for l2 in pot_prods:
                                # get pairs
                                if l1.get_number_fas() < l2.get_number_fas():
                                    f1 = l1.get_fas()
                                    f2 = l2.get_fas()
                                else:
                                    f2 = l1.get_fas()
                                    f1 = l2.get_fas()
                                for ff2 in range(len(f2)):
                                    if sorted(f2) == sorted(f1 + [f2[ff2]]):
                                        edge_list.add_edge(
                                            Edge(l1, l2, enzyme_id=i.get_enzyme_id(), reaction_id=str(curr_reac_id),
                                                 reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                                                 gene_name=i.get_gene_name(),
                                                 fa_param=str(f2[ff2]),
                                                 nl_participants=i.get_nl_participants()))
                                        curr_reac_id += 1
                                        break
                    # This is only for reaction transforming lipids into ether lipids
                    elif i.get_reaction_type() == L_FAether:
                        sub_ref = i.get_substrates()[0]
                        prod_ref = i.get_products()[0]

                        if (sub_ref.get_headgroup() == prod_ref.get_headgroup()) and \
                            (sub_ref.get_fas() == prod_ref.get_fas()) and \
                                (sub_ref.get_lcb() == prod_ref.get_lcb()):
                            if (sub_ref.get_ether() == (prod_ref.get_ether()+1)) or \
                                    (prod_ref.get_ether() == (sub_ref.get_ether() + 1)):
                                for l1 in pot_subs:
                                    for l2 in pot_prods:
                                        if sorted([x.as_not_ether() for x in l1.get_fas()]) == \
                                            sorted([x.as_not_ether() for x in l2.get_fas()]):
                                            edge_list.add_edge(
                                                Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                                                     reaction_id=str(curr_reac_id),
                                                     reaction_type=i.get_reaction_type(),
                                                     notes="",
                                                     uniprot=i.get_uniprot(),
                                                     gene_name=i.get_gene_name(),
                                                     fa_param=l1.sum_length(),
                                                     nl_participants=i.get_nl_participants()))
                                            curr_reac_id += 1
                                            break



            elif i.shape() == (1, 2) or i.shape() == (2, 1):
                if i.get_reaction_type() == L_FAdelete:
                    twos = i.get_substrates() if len(i.get_substrates()) == 2 else i.get_products()
                    ones = i.get_substrates() if len(i.get_substrates()) == 1 else i.get_products()
                    one = ones[0]
                    t1 = twos[0]
                    t2 = twos[1]
                    # find partner
                    if (one.get_headgroup() == t1.get_headgroup()) and (one.get_lcb() == t1.get_lcb()) and \
                            (one.get_ether() == t1.get_ether()) and (one.get_fas() == (t1.get_fas()+1)):
                        partner = t1
                        other = t2
                    else:
                        partner = t2
                        other = t1
                    if one.get_abbr() in lip_dict and partner.get_abbr() in lip_dict and \
                            other.get_abbr() in lip_dict:
                        one_pos = lip_dict[one.get_abbr()]
                        partner_pot = lip_dict[partner.get_abbr()]
                        other_pot = lip_dict[other.get_abbr()]
                        for l1 in one_pos:
                            for l2 in partner_pot:
                                for l3 in other_pot:
                                    for fa in l3.get_fas():
                                        if sorted(l1.get_fas()) == sorted(l2.get_fas() + [fa]):
                                            edge_list.add_edges([Edge(l1, l2,
                                                                      enzyme_id=i.get_enzyme_id(),
                                                                      reaction_id=str(curr_reac_id),
                                                                      reaction_type=i.get_reaction_type(),
                                                                      notes="", uniprot=i.get_uniprot(),
                                                                      gene_name=i.get_gene_name(),
                                                                      reaction_structure="1,2",
                                                                      l1_type="substrate", l2_type="product",
                                                                      fa_param=str(fa),
                                                                      nl_participants=i.get_nl_participants()),
                                                                 # Makes only sense in bipartite networks...
                                                                 Edge(l1, l3,
                                                                      enzyme_id=i.get_enzyme_id(),
                                                                      reaction_id=str(curr_reac_id),
                                                                      reaction_type=i.get_reaction_type(),
                                                                      notes="", uniprot=i.get_uniprot(),
                                                                      gene_name=i.get_gene_name(),
                                                                      reaction_structure="1,2",
                                                                      l1_type="substrate", l2_type="product",
                                                                      fa_param=str(fa),
                                                                      nl_participants=i.get_nl_participants())
                                                                 ]
                                                )

                                            curr_reac_id += 1
                                            break
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
                                        edge_list.add_edge(
                                            Edge(l1, l2, enzyme_id=i.get_enzyme_id(), reaction_id=str(curr_reac_id),
                                                 reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                                                 gene_name=i.get_gene_name(),
                                                 reaction_structure="1,2",
                                                 l1_type="substrate", l2_type="product",
                                                 fa_param=str(l2.sum_length()),
                                                 nl_participants=i.get_nl_participants()))
                                        edge_list.add_edge(
                                            Edge(l1, l3, enzyme_id=i.get_enzyme_id(), reaction_id=str(curr_reac_id),
                                                 reaction_type=i.get_reaction_type(), notes="", uniprot=i.get_uniprot(),
                                                 gene_name=i.get_gene_name(),
                                                 reaction_structure="1,2",
                                                 l1_type="substrate", l2_type="product",
                                                 fa_param=str(l2.sum_length()),
                                                 nl_participants=i.get_nl_participants()))
                                        curr_reac_id += 1
                                        break
            elif i.shape() == (2, 2):
                subs = i.get_substrates()
                prods = i.get_products()
                if i.get_reaction_type() == L_FAdelete:
                    if subs[0].get_headgroup() == prods[0].get_headgroup() and \
                            subs[0].get_lcb() == prods[0].get_lcb() and \
                            subs[0].get_ether() == prods[0].get_ether() and \
                            subs[0].get_potentialfas() == prods[0].get_potentialfas() and \
                            ((subs[0].get_fas() == (prods[0].get_fas()+1) or
                              (prods[0].get_fas() == (subs[0].get_fas()+1)))):
                        p11 = subs[0]
                        p12 = prods[0]
                        p21 = subs[1]
                        p22 = prods[1]
                    else:
                        p11 = subs[0]
                        p12 = prods[1]
                        p21 = subs[1]
                        p22 = prods[0]

                    # get higher partner p1
                    if p11.get_fas() > p12.get_fas():
                        higher_p1 = p11
                        lower_p1 = p12
                    else:
                        higher_p1 = p12
                        lower_p1 = p11

                    #get higher partner p2
                    if p21.get_fas() > p22.get_fas():
                        higher_p2 = p21
                        lower_p2 = p22
                    else:
                        higher_p2 = p22
                        lower_p2 = p21


                    if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and \
                            p21.get_abbr() in lip_dict and p22.get_abbr() in lip_dict:

                        # Uncoupling 2,2 L_FAdelete reactions for local search

                        for l1 in lip_dict[higher_p1.get_abbr()]:
                            for l2 in lip_dict[lower_p1.get_abbr()]:
                                for c1 in itertools.combinations(l1.get_fas(), l1.get_number_fas()-1):
                                    if sorted(list(c1)) == sorted(l2.get_fas()):
                                        for fa1 in l1.get_fas():
                                            if sorted([fa1] + list(c1)) == sorted(l1.get_fas()):
                                                edge_list.add_edges([Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                                                                          reaction_id=str(curr_reac_id),
                                                                          reaction_type=i.get_reaction_type(),
                                                                          notes="", uniprot=i.get_uniprot(),
                                                                          gene_name=i.get_gene_name(),
                                                                          reaction_structure="2,2",
                                                                          l1_type="substrate",
                                                                          l2_type="product",
                                                                          fa_param=str(fa1),
                                                                          nl_participants=i.get_nl_participants()
                                                                          )])
                                                curr_reac_id += 1
                                    break

                        for l1 in lip_dict[higher_p2.get_abbr()]:
                            for l2 in lip_dict[lower_p2.get_abbr()]:
                                for c1 in itertools.combinations(l1.get_fas(), l1.get_number_fas()-1):
                                    if sorted(list(c1)) == sorted(l2.get_fas()):
                                        for fa1 in l1.get_fas():
                                            if sorted([fa1] + list(c1)) == sorted(l1.get_fas()):
                                                edge_list.add_edges([Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                                                                          reaction_id=str(curr_reac_id),
                                                                          reaction_type=i.get_reaction_type(),
                                                                          notes="", uniprot=i.get_uniprot(),
                                                                          gene_name=i.get_gene_name(),
                                                                          reaction_structure="2,2",
                                                                          l1_type="substrate",
                                                                          l2_type="product",
                                                                          fa_param=str(fa1),
                                                                          nl_participants=i.get_nl_participants()
                                                                          )])
                                                curr_reac_id += 1
                                    break

                        # for l1 in lip_dict[higher_p1.get_abbr()]:
                        #     for l2 in lip_dict[lower_p1.get_abbr()]:
                        #         for c1 in itertools.combinations(l1.get_fas(), l1.get_number_fas()-1):
                        #             if sorted(list(c1)) == sorted(l2.get_fas()):
                        #                 for fa1 in l1.get_fas():
                        #                     if sorted([fa1] + list(c1)) == sorted(l1.get_fas()):
                        #                         for l3 in lip_dict[higher_p2.get_abbr()]:
                        #                             if fa1 in l3.get_fas():
                        #                                 for l4 in lip_dict[lower_p2.get_abbr()]:
                        #                                     fa_set = set(
                        #                                         l1.get_fas() + l2.get_fas() + l3.get_fas() + l4.get_fas())
                        #                                     for fa in fa_set:
                        #                                         if (sorted(l1.get_fas()) == sorted(
                        #                                                 l2.get_fas() + [fa]) or
                        #                                             sorted(l1.get_fas() + [fa]) == sorted(
                        #                                                     l2.get_fas())) and \
                        #                                                 (sorted(l3.get_fas()) == sorted(
                        #                                                     l4.get_fas() + [fa]) or
                        #                                                  sorted(l3.get_fas() + [fa]) == sorted(
                        #                                                             l4.get_fas())):
                        #
                        #                                             edge_list.add_edges([Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                        #                                                          reaction_id=str(curr_reac_id),
                        #                                                          reaction_type=i.get_reaction_type(),
                        #                                                          notes="", uniprot=i.get_uniprot(),
                        #                                                          gene_name=i.get_gene_name(),
                        #                                                          reaction_structure="2,2",
                        #                                                          l1_type="substrate",
                        #                                                          l2_type="product",
                        #                                                          fa_param=str(fa1),
                        #                                                          nl_participants=i.get_nl_participants()
                        #                                                                       ),
                        #                                                     Edge(l3, l4, enzyme_id=i.get_enzyme_id(),
                        #                                                          reaction_id=str(curr_reac_id),
                        #                                                          reaction_type=i.get_reaction_type(),
                        #                                                          notes="", uniprot=i.get_uniprot(),
                        #                                                          gene_name=i.get_gene_name(),
                        #                                                          reaction_structure="2,2",
                        #                                                          l1_type="substrate",
                        #                                                          l2_type="product",
                        #                                                          fa_param=str(fa1),
                        #                                                          nl_participants=i.get_nl_participants()
                        #                                                          )
                        #                                                                  ])
                        #                                             curr_reac_id += 1
                        #
                        #
                        #                         break

                    # if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and \
                    #         p21.get_abbr() in lip_dict and p22.get_abbr() in lip_dict:
                    #     for l1 in lip_dict[p11.get_abbr()]:
                    #         for l2 in lip_dict[p12.get_abbr()]:
                    #
                    #             for l3 in lip_dict[p21.get_abbr()]:
                    #                 edge_list.add_edges(lfad22_inner(i, lip_dict[p22.get_abbr()], l1, l2, l3, rid=curr_reac_id))
                    #                 curr_reac_id += 1

                elif i.get_reaction_type() == L_HGdelete or i.get_reaction_type() == L_HGmodify:
                    # TODO: Currently not working for complex L_HGmodify reactions,
                    #  e.g. parts of an headgroup is added to another one
                    if subs[0].get_headgroup() == prods[0].get_headgroup() and \
                            subs[0].get_lcb() == prods[1].get_lcb() and subs[0].get_ether() == prods[1].get_ether():
                        p11 = subs[0] # partner: (p11, p12) and (p21, p22)
                        p12 = prods[1]
                        p21 = subs[1]
                        p22 = prods[0]
                    else:
                        p11 = subs[0]
                        p12 = prods[0]
                        p21 = subs[1]
                        p22 = prods[1]
                    if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and \
                            p21.get_abbr() in lip_dict and p22.get_abbr() in lip_dict:
                        # Evaluate first partner set (p11, p12):
                        for l1 in lip_dict[p11.get_abbr()]:
                            for l2 in lip_dict[p12.get_abbr()]:
                                if sorted(l1.get_fas()) == sorted(l2.get_fas()):
                                    edge_list.add_edge(Edge(l1, l2, enzyme_id=i.get_enzyme_id(),
                                                            reaction_id=str(curr_reac_id),
                                                            reaction_type=i.get_reaction_type(), notes="",
                                                            uniprot=i.get_uniprot(),
                                                            gene_name=i.get_gene_name(),
                                                            reaction_structure="2,2",
                                                            l1_type="substrate",
                                                            l2_type="product",
                                                            set_id=1,
                                                            fa_param=str(l1.sum_length()+l2.sum_length()),
                                                            nl_participants=i.get_nl_participants())
                                                            )

                                    curr_reac_id += 1
                                    break
                        # Evaluate second partner set (p21, p22):
                        for l3 in lip_dict[p21.get_abbr()]:
                            for l4 in lip_dict[p22.get_abbr()]:
                                if sorted(l3.get_fas()) == sorted(l4.get_fas()):
                                    edge_list.add_edge(Edge(l3, l4, enzyme_id=i.get_enzyme_id(),
                                                            reaction_id=str(curr_reac_id),
                                                            reaction_type=i.get_reaction_type(),
                                                            notes="", uniprot=i.get_uniprot(),
                                                            gene_name=i.get_gene_name(),
                                                            reaction_structure="2,2",
                                                            l1_type="substrate",
                                                            l2_type="product",
                                                            set_id=2,
                                                            fa_param=str(l3.sum_length()+l4.sum_length()),
                                                            nl_participants=i.get_nl_participants()))

                                    curr_reac_id += 1
                                    break

                    # old:
                    # if p11.get_abbr() in lip_dict and p12.get_abbr() in lip_dict and \
                    #         p21.get_abbr() in lip_dict and p22.get_abbr() in lip_dict:
                    #     for l1 in lip_dict[p11.get_abbr()]:
                    #         for l2 in lip_dict[p12.get_abbr()]:
                    #             for l3 in lip_dict[p21.get_abbr()]:
                    #                 edge_list.add_edges(lhg22_inner(i, lip_dict[p22.get_abbr()], l1, l2, l3))
    return edge_list

def evaluate_fa_reactions_static(lip_dict: Dict[str, List[Lipid]],
                                 fa_reacs: List[FAReaction],
                                 excluded_fa_conversions: List[List[FA]] = None, startid=0) -> Edgelist:
    curr_reac_id = startid
    edge_list = Edgelist()
    for far in fa_reacs:
        for lip in lip_dict.keys():
            if len(lip_dict[lip]) > 1:
                ll = lip_dict[lip]
                for l1 in range(len(ll) - 1):
                    for l2 in range(l1 + 1, len(ll)):
                        if far.is_transformable(ll[l1], ll[l2], excluded_reactions=excluded_fa_conversions):
                            edge_list.add_edge(Edge(ll[l1], ll[l2], enzyme_id="", reaction_id=str(curr_reac_id),
                                                    reaction_type=L_FAmodify, notes=far.get_last_conversion()))
                            curr_reac_id += 1
    return edge_list


def evaluate_class_reactions_worker(queue: Queue, class_reacs: List[Reaction],
                                    lip_dict: Dict[str, List[Lipid]]) -> int:
    queue.put(evaluate_class_reactions_static(class_reacs, lip_dict))
    return 0


def evaluate_fa_reactions_worker(queue: Queue, lip_dict: Dict[str, List[Lipid]],
                                 fa_reacs: List[FAReaction],
                                 excluded_fa_conversions: List[List[FA]] = None) -> int:
    queue.put(evaluate_fa_reactions_static(lip_dict, fa_reacs, excluded_fa_conversions))
    return 0

def evaluate_ether_conversions_static(lip_dict: Dict[str, List[Lipid]],
                                     reference_lipids: List[ReferenceLipid],
                                     startid: int = 0) -> Edgelist:
    curr_reac_id = startid
    edge_list = Edgelist()
    for i in range(len(reference_lipids)):
        for j in range(i+1, len(reference_lipids)):
            sub = reference_lipids[i]
            prod = reference_lipids[j]
            if sub.get_abbr() in lip_dict.keys() and prod.get_abbr() in lip_dict.keys():
                if (((sub.get_ether()-1) == prod.get_ether())
                        or (sub.get_ether() == (prod.get_ether()))-1) \
                       and (sub.get_lcb() == prod.get_lcb()) \
                       and (sub.get_potentialfas() == prod.get_potentialfas()) \
                       and (sub.get_headgroup() == prod.get_headgroup()) \
                       and ((sub.get_fas()) == prod.get_fas()):
                    for l1 in lip_dict[sub.get_abbr()]:
                        for l2 in lip_dict[prod.get_abbr()]:
                            if sorted([x.as_not_ether() for x in l1.get_fas()]) == \
                                    sorted([x.as_not_ether() for x in l2.get_fas()]):
                                edge_list.add_edge(
                                    Edge(l1, l2, enzyme_id="",
                                         reaction_id=str(curr_reac_id),
                                         reaction_type=L_FAmodify,
                                         notes="",
                                         uniprot="",
                                         gene_name="",
                                         fa_param=""))
                                curr_reac_id += 1
                                break

    return edge_list
