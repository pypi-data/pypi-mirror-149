import importlib.resources as pkg_resources
import pandas as pd
from . import data

with pkg_resources.path(data, "Reactome_ConnectionOfReactionsToMolecule_all.csv") as path:
    REACTOME_REACTION_TO_MOLECULE = pd.read_csv(path)

with pkg_resources.path(data, "Reactome_Others_all_unique.csv") as path:
    REACTOME_OTHERS_UNIQUE = pd.read_csv(path)

with pkg_resources.path(data, "Reactome_ReactionDetailsEnzyme_all.csv") as path:
    REACTOME_REACTION_DETAILS = pd.read_csv(path)

with pkg_resources.path(data, "Reactome_reactions_for_curation.csv") as path:
    REACTOME_REACTION_CURATION = pd.read_csv(path)

with pkg_resources.path(data, "Rhea_ConnectionOfReactionsToMolecule_all.csv") as path:
    RHEA_REACTION_TO_MOLECULE = pd.read_csv(path)

with pkg_resources.path(data, "Rhea_Others_all_unique.csv") as path:
    RHEA_OTHERS_UNIQUE = pd.read_csv(path)

with pkg_resources.path(data, "Rhea_reactions_for_curation.csv") as path:
    RHEA_REACTION_CURATION = pd.read_csv(path)

with pkg_resources.path(data, "Rhea_GeneName_mapping.csv") as path:
    RHEA_MAPPING = pd.read_csv(path).set_index("RHEA_ID")

with pkg_resources.path(data, "standard_lipid_classes.csv") as path:
    STANDARD_LIPID_CLASSES = pd.read_csv(path)
