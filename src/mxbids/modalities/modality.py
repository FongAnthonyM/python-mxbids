"""modality.py
A base class for BIDS Modalities.
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
from collections.abc import MutableMapping
from collections import ChainMap
from copy import deepcopy
from pathlib import Path
from typing import ClassVar, Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseBIDSDirectory, BaseImporter, BaseExporter


# Definitions #
# Classes #
class Modality(BaseBIDSDirectory):
    """A base class for BIDS Modalities.

    Class Attributes:
        _module_: The module name for this class.
        class_register: A register of class types.
        class_registration: Indicates if the class should be registered.
        default_meta_information: Default meta information for the modality.
        
    Attributes:
        subject_name: The name of the subject associated with this modality.
        session_name: The name of the session associated with this modality.
        importers: Mapping of importers.
        exporters: Mapping of exporters.
        
    Args:
        path: The path to the modality's directory.
        name: The name of the modality.
        parent_path: The path to the parent directory.
        mode: The file mode to set for the modality.
        create: Determines if this modality will be created if it does not exist.
        build: Determines if the directory will be built after creation.
        load: Determines if the modality will load.
        init: Determines if this object will construct.
        **kwargs: Additional keyword arguments.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.modalities"

    class_register: ClassVar[dict[str, dict[str, type]]] = {}
    class_registration: ClassVar[bool] = True
    default_meta_information: ClassVar[dict[str, Any]] = deepcopy(BaseBIDSDirectory.default_meta_information) | {
        "Type": "Modality",
    }

    # Class Methods #
    @classmethod
    def generate_meta_information_path(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
    ) -> Path:
        """Gets a class namespace and name from a given set of arguments.

        Args:
            path: The path to the session.
            name: The name of the session.
            parent_path: The path to the parent of the session.

        Returns:
            The path to the meta information file.

        Raises:
            ValueError: If neither path nor (parent_path and name) are provided.
        """
        if path is not None:
            if not isinstance(path, Path):
                path = Path(path)

            if name is None:
                name = path.stem
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to dispatch class.")

        subject_name = path.parts[-3][4:]
        session_name = path.parts[-2][4:]

        return path / f"sub-{subject_name}_ses-{session_name}_{name}_meta.json"

    # Attributes #
    subject_name: str | None = None
    session_name: str | None = None

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Modality."""
        return self.name

    @property
    def full_name(self) -> str:
        """The full name of this Modality."""
        return f"sub-{self.subject_name}_ses-{self.session_name}"

    @property
    def meta_information_path(self) -> Path | None:
        """The path to the meta information json file."""
        return None if self._path is None else self._path / f"{self.full_name}_{self.name}_meta.json"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = True,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
                create=create,
                build=build,
                load=load,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the modality's directory.
            name: The name of the modality.
            parent_path: The path to the parent directory.
            mode: The file mode to set for the modality.
            create: Determines if this modality will be created if it does not exist.
            build: Determines if the directory will be built after creation.
            load: Determines if the modality will load.
            **kwargs: Additional keyword arguments.
        """
        # Name and Path Resolution
        if name is not None:
            self.name = name

        if path is not None:
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        if self.path is not None:
            if name is None:
                self.name = self.path.stem
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / self.directory_name

        if self.path is not None:
            self.subject_name = self.path.parts[-3][4:]
            self.session_name = self.path.parts[-2][4:]

        # Create or Load
        if self.path is not None:
            if not self.path.exists():
                if create:
                    self.create(build=build)
            elif load:
                self.load()

        # Construct Parent #
        super().construct(**kwargs)