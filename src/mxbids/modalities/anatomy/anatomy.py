"""anatomy.py
A BIDS Anatomy Modality.
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
from collections.abc import MutableMapping
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister

# Local Packages #
from ...base import BaseImporter, BaseExporter
from ..modality import Modality


# Definitions #
# Classes #
class Anatomy(Modality):
    """A BIDS Anatomy Modality.

    Class Attributes:
        _module_: The module name for this class.
        class_register_namespace: The namespace for class registration.

    Attributes:
        component_types_register: Register for component types.
        name: The name of the modality.
        importers: Mapping of importers.
        exporters: Mapping of exporters.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.modalities"
    class_register_namespace: ClassVar[str | None] = "mxbids.anat"

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    name: str = "anat"

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = Modality.importers.new_child()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = Modality.exporters.new_child()
