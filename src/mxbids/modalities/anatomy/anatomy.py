"""anatomy.py
A BIDS Anatomy Modality.
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
