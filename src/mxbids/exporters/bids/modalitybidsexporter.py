"""modalitybidsexporter.py
A class for exporting BIDS modalities.
"""

# Header #
__package_name__ = "mxbids"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__maintainer__ = "Anthony Fong"
__email__ = ""

__copyright__ = "Copyright 2022, Anthony Fong"
__license__ = "MIT"

__version__ = "0.3.0"
__status__ = "Development Status :: 3 - Alpha"


# Imports #
# Standard Libraries #

# Third-Party Packages #

# Local Packages #
from ...modalities import Modality
from ..modalityexporter import ModalityExporter


# Definitions #
# Classes #
class ModalityBIDSExporter(ModalityExporter):
    """A class for exporting BIDS modalities."""

    # Attributes #
    exporter_name: str = "BIDS"
    export_exclude_names: set[str, ...] = {"meta"}


# Assign Exporter
Modality.exporters["BIDS"] = (ModalityBIDSExporter, {})
