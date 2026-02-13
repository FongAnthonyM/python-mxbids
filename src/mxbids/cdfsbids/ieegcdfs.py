"""ieegcdfs.py
A BIDS IEEG CDFS Modality.
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
from typing import ClassVar, Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseImporter, BaseExporter
from ..modalities import IEEG
from .ieegcdfscomponent import IEEGCDFSComponent


# Definitions #
# Classes #
class IEEGCDFS(IEEG):
    """A BIDS IEEG CDFS Modality.

    Class Attributes:
        _module_: The module name for this class.
        default_component_types: Default component types for the modality.

    Attributes:
        importers: Mapping of importers.
        exporters: Mapping of exporters.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.cdfsbids"
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "cdfs": (IEEGCDFSComponent, {}),
    }
