# This file includes code from:
# LINEX webtool
# Copyright (C) 2021  LipiTUM group, Chair of experimental Bioinformatics, Technical University of Munich
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Dict, List, Union
import numpy as np
import warnings

# From package
from .lipid import Lipid
from .parser import lipid_parser
from .GenerateLipidNetwork import lipid_attributes


def _get_weighted_lipid_dict(self) -> Dict[str, List[Lipid]]:
    lipid_dict = self.gln.get_lipid_dict()
    for cls in lipid_dict.keys():
        tmp_weights = {}
        # Count how often a lipid from the same dataname exists in the data
        for lip in lipid_dict[cls]:
            if lip.get_dataname() in tmp_weights.keys():
                tmp_weights[lip.get_dataname()] += 1
            else:
                tmp_weights[lip.get_dataname()] = 1
        # Use these counts as factors
        for lipi in range(len(lipid_dict[cls])):
            lipid_dict[cls][lipi].set_div_factor(tmp_weights[lipid_dict[cls][lipi].get_dataname()])

    return lipid_dict


def add_lipid(self, new_lipid: Union[str, List[str], Lipid, List[Lipid]],
              compute_new_edgelist: bool = True,
              is_lm_compatible: bool = False):
    """
    Adding one or multiple new lipid(s) to the network.
    Please note: compute_*_network has to be called separately after
    new lipids have been added

    Parameters
    ----------
    :param new_lipid : Union[str, Iterable[str], Lipid, Iterable[Lipid]]
        Lipid(s) to add to the network. These can be lipid class objects or
        lipid names as str, which can then be parsed into Lipid objects

    :param compute_new_edgelist : bool, optional, default True
        Whether to recompute the edgelist based on the new
        lipid set

    :param prl : bool, optional, default True
        Whether to compute the edgelist in a parallelized fashion

    :param is_lm_compatible: cool, optional, default = False
        When the lipids in the data file are not compatible with the LIPID MAPS nomenclature,
        they can be converted with LipidLynxX. If the parameter is False,
        lipids will be converted before (This can take up to several minutes).
        If True, the lipids won't be converted.
        For more information visit the LipidLynxX website: https://www.lipidmaps.org/lipidlynxx/

    Raises
    ------
    ValueError
        If new_lipid is not a Lipid object or a list of Lipid object
    """
    # Converted lipids
    nl = []

    if isinstance(new_lipid, List):
        if isinstance(new_lipid[0], Lipid):
            for lipid in new_lipid:
                self.gln.add_new_lipid(lipid)
            nl = new_lipid
        if isinstance(new_lipid[0], str):
            for lipid in new_lipid:
                tmp_lipid = lipid_parser(lipid,
                                         self._ref_dict,
                                         is_ll_compatible=is_lm_compatible,
                                         org_name=lipid)
                self.gln.add_new_lipid(tmp_lipid)
                nl.append(tmp_lipid)

    elif isinstance(new_lipid, str):
        # Parse lipid from str
        tmp_lipid = lipid_parser(new_lipid,
                                 self._ref_dict,
                                 is_ll_compatible=is_lm_compatible,
                                 org_name=new_lipid)
        self.gln.add_new_lipid(tmp_lipid)
        nl = [tmp_lipid]
    else:
        if not isinstance(new_lipid, Lipid):
            raise ValueError(
                "'new_lipid' must be an object of class 'Lipid' or 'str'"
                f"or a list of 'Lipid' or 'str' objects, not {type(new_lipid).__name__}"
            )
        self.gln.add_new_lipid(new_lipid)
        nl = [new_lipid]
    # TODO: add computed properties and colours for new_lipid
    for lip in nl:
        lipid_attrs = lipid_attributes(lip)
        for attr in self._attributes_to_plot["nodes"]:
            if self._attr_group_size_[attr] == 0:
                if self.lipid_attributes.get(attr) is not None:
                    if self.last_network_call.get('network', '') == "native":
                        self.lipid_attributes[attr][lip.get_native_string()] = lipid_attrs.get(attr, np.nan)
                    else:
                        self.lipid_attributes[attr][str(lip)] = lipid_attrs.get(attr, np.nan)
    # recompute edgelist:
    if compute_new_edgelist:
        # NOTE: currently edge attributes are NOT reset,
        # because self.network is not necessarily changed
        # self._reset_edges_()
        self.gln.compute_edgelist()
        if self.last_network_call:
            self.last_network_call['force_overwrite'] = True
            self._compute_network_(**self.last_network_call)
        else:
            warnings.warn(
                'No network computed yet!'
            )


def all_molecular_species_lipids(self) -> List[str]:
    """
    Converts the internal "__lipids" dict into a list of (molecular species) string representations of all lipids.
    :return: List of string representations of molecular species lipids
    """
    out_l = []
    lip_dict = self.gln.get_lipid_dict()
    for cls in lip_dict:
        # FIXME: how to get the correct lipid name(s) here?
        out_l += [str(x) for x in lip_dict[cls]]
    return out_l


def all_native_lipids(self) -> List[str]:
    """
    Converts the internal "__lipids" dict into a list of (sum species) string representations of all lipids.
    :return: List of string representations of sum species lipids
    """
    out_l = []
    lip_dict = self.gln.get_lipid_dict()
    for cls in lip_dict:
        out_l += [x.get_native_string() for x in lip_dict[cls]]
    return out_l


def all_lipid_objects(self) -> List[Lipid]:
    out_l = []
    lip_dict = self.gln.get_lipid_dict()
    for cls in lip_dict:
        out_l += [x for x in lip_dict[cls]]
    return out_l


def get_incompatible_lipids(self) -> List[str]:
    """
    Get all incompatible lipids.

    These lipids were not parsed/identified correctly and therefore removed from the data.

    :return: List of removed lipids (column names) from the data.
    """
    return self._incompatible_lipids
