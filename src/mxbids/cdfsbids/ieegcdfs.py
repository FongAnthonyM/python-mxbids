"""ieegcdfs.py
A BIDS IEEG CDFS Modality.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


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
