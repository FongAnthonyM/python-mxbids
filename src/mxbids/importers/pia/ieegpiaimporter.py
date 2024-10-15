"""ieegpiaimporter.py
A BIDS iEEG PIA Importer.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

# Third-Party Packages #
import pandas as pd
from scipy.io import loadmat

# Local Packages #
from ..modalityimporter import ModalityImporter


# Definitions #
# Classes #
class IEEGPiaImporter(ModalityImporter):
    """A BIDS iEEG PIA Importer."""

    # Static Methods #
    @staticmethod
    def convert_electrodes(old_path: Path, new_path: Path) -> None:
        """Converts electrode data from a MATLAB file to a BIDS-compliant TSV file.

        Args:
            old_path: The path to the original MATLAB file.
            new_path: The path to the new TSV file.
        """
        original_montage = loadmat(old_path.as_posix(), squeeze_me=True)
        xyz = original_montage["elecmatrix"]
        eleclabels = original_montage["eleclabels"]
        eleclabels = eleclabels[: len(xyz), :]

        bids_montage = pd.DataFrame(
            columns=[
                "name",
                "x",
                "y",
                "z",
                "size",
                "material",
                "manufacturer",
                "group",
                "hemisphere",
                "type",
                "impedance",
            ]
        )
        bids_montage.loc[:, "x"] = xyz[:, 0]
        bids_montage.loc[:, "y"] = xyz[:, 1]
        bids_montage.loc[:, "z"] = xyz[:, 2]
        bids_montage.loc[:, "name"] = eleclabels[:, 0]
        bids_montage.loc[:, "group"] = eleclabels[:, 2]
        bids_montage.loc[:, "size"] = "n/a"
        bids_montage.loc[:, "material"] = "n/a"
        bids_montage.loc[:, "manufacturer"] = "n/a"
        bids_montage.loc[bids_montage["x"] > 0, "hemisphere"] = "r"
        bids_montage.loc[bids_montage["x"] <= 0, "hemisphere"] = "l"
        bids_montage.loc[:, "type"] = "n/a"
        bids_montage.loc[:, "impedance"] = "n/a"
        bids_montage.name = bids_montage.name.fillna("NaN")

        bids_montage.to_csv(new_path, sep="\t")

    # Attributes #
    importer_name: str = "Pia"

    file_maps: list[tuple[str, str, Iterable[Path], Callable, dict[str, Any]]] = [
        (
            "electrodes",
            ".tsv",
            (Path("elecs/clinical_elecs_all.mat"), Path("elecs/clinical_TDT_elecs_all.mat"), Path("elecs/clinical_elecs_all1.mat")),
            convert_electrodes,
            {},
        ),
    ]
