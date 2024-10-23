"""anatomybidsexporter.py
A class for exporting BIDS anatomy data.
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

# Third-Party Packages #

# Local Packages #
from ...modalities import Anatomy
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class AnatomyBIDSExporter(ModalityBIDSExporter):
    """A class for exporting BIDS anatomy data."""

    # Attributes #
    exporter_name: str = "BIDS"
    export_exclude_names: set[str, ...] = {"meta"}


# Assign Exporter
Anatomy.exporters["BIDS"] = (AnatomyBIDSExporter, {})
