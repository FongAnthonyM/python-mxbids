"""ieegupennexporter.py
A class for exporting UPENN iEEG data.
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
from xltektools.xltekmxbids.modalities.exporters.ieegxltekbidsexporter import IEEGXLTEKBIDSExporter


# Definitions #
# Classes #
class IEEGUPENNExporter(IEEGXLTEKBIDSExporter):
    """A class for exporting UPENN iEEG data."""

    # Attributes #
    exporter_name: str = "UPENN"
    export_file_names = {"coordsystem.json", "electrodes.tsv"}
