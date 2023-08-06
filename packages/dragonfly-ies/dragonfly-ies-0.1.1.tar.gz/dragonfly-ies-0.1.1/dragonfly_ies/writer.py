import pathlib

from honeybee_ies.writer import model_to_ies as hb_model_to_ies
from dragonfly.model import Model


def model_to_ies(
        model: Model, folder: str = '.', name: str = None, enforce_adj: bool = True
    ) -> pathlib.Path:
    """Export a dragonfly model to an IES GEM file.

    Args:
        model: A dragonfly model.
        folder: Path to target folder to export the file. Default is current folder.
        name: An optional name for exported file. By default the name of the model will
            be used.
        enforce_adj: Boolean to note whether an exception should be raised if
            an adjacency between two Room2Ds is invalid (True) or if the invalid
            Surface boundary condition should be replaced with an Outdoor
            boundary condition (False). (Default: True).

    Returns:
        Path to exported GEM file.
    """
    hb_models = model.to_honeybee(
        object_per_model='District', use_multiplier=False,
        solve_ceiling_adjacencies=False, enforce_adj=enforce_adj
    )
    return hb_model_to_ies(hb_models[0], folder, name)
