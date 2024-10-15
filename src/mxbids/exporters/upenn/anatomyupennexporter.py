"""anatomyupennexporter.py
A class for exporting UPENN anatomy data.
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
from ..bids import AnatomyBIDSExporter


# Definitions #
# Classes #
class AnatomyUPENNExporter(AnatomyBIDSExporter):
    """A class for exporting UPENN anatomy data."""

    # Attributes #
    exporter_name: str = "UPENN"
