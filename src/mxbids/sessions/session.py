"""session.py
A BIDS Session.
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
from collections.abc import Iterable, MutableMapping
from collections import ChainMap
from copy import deepcopy
from pathlib import Path
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister

# Local Packages #
from ..base import BaseBIDSDirectory, BaseImporter, BaseExporter
from ..modalities import Modality


# Definitions #
# Classes #
class Session(BaseBIDSDirectory):
    """A BIDS Session.

    Class Attributes:
        _module_: The module name for this class.
        class_register: A register of class types.
        class_registration: Indicates if the class should be registered.
        class_register_namespace: The namespace for class registration.
        default_meta_information: Default meta information for the session.
        default_modalities: Default modalities for the session.
        
    Attributes:
        component_types_register: Register for component types.
        subject_name: The name of the subject associated with this session.
        importers: Mapping of importers.
        exporters: Mapping of exporters.
        modalities: Dictionary of modalities.

    Args:
        path: The path to the session's directory.
        name: The ID name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        build: Determines if the directory will be built after creation.
        load: Determines if the modalities will be loaded from the session's directory.
        modalities_to_load: List of modality names to load.
        init: Determines if this object will construct.
        **kwargs: Additional keyword arguments.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.sessions"

    class_register: ClassVar[dict[str, dict[str, type]]] = {}
    class_registration: ClassVar[bool] = True
    class_register_namespace: ClassVar[str | None] = "mxbids"
    default_meta_information: ClassVar[dict[str, Any]] = deepcopy(BaseBIDSDirectory.default_meta_information) | {
        "Type": "Session",
    }
    default_modalities: ClassVar[dict[str, tuple[type[Modality], dict[str, Any]]]] = {}

    # Class Methods #
    @classmethod
    def generate_meta_information_path(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
    ) -> Path:
        """Generates the meta information path for the session.

        Args:
            path: The path to the session's directory. Defaults to None.
            name: The name of the session. Defaults to None.
            parent_path: The path to the parent directory. Defaults to None.

        Returns:
            The path to the meta information file.

        Raises:
            ValueError: If neither path nor (parent_path and name) are provided.
        """
        if path is not None:
            if not isinstance(path, Path):
                path = Path(path)

            if name is None:
                name = path.stem[4:]
        elif parent_path is not None and name is not None:
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"ses-{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to dispatch class.")

        parent_name = path.parts[-2][4:]

        return path / f"sub-{parent_name}_ses-{name}_meta.json"

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    subject_name: str | None = None

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    modalities: dict[str, Any] = {}

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Session."""
        return f"ses-{self.name}"

    @property
    def full_name(self) -> str:
        """The full name of this Session."""
        return f"sub-{self.subject_name}_ses-{self.name}"

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
        modalities_to_load: list[str] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.modalities = {}

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
                modalities_to_load=modalities_to_load,
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
        modalities_to_load: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs the Session object.
    
        Args:
            path: The path to the session's directory.
            name: The ID name of the session.
            parent_path: The parent path of this session.
            mode: The file mode to set this session to.
            create: Determines if this session will be created if it does not exist.
            build: Determines if the directory will be built after creation.
            load: Determines if the session will load.
            modalities_to_load: List of modality names to load.
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
                self.name = self.path.stem[4:]
        elif parent_path is not None and self.name is not None:
            self.path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / self.directory_name
    
        if self.path is not None:
            self.subject_name = self.path.parts[-2][4:]
    
        # Load
        if self.path is not None and self.path.exists():
            if load:
                self.load()
        elif create:
            self.construct_modalities()
    
        # Construct Parent
        super().construct(**kwargs)
    
        # Create
        if self.path is not None and not self.path.exists() and create:
            self.create(build=build)

    def build(self) -> None:
        """Builds the session and its modalities."""
        super().build()
        self.build_modalities()
    
    def load(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        """Loads the session and its modalities.
    
        Args:
            names: Names of modalities to load.
            mode: File mode to set the modalities to.
            load: Whether to load the modalities.
            **kwargs: Additional keyword arguments.
        """
        super().load()
        self.load_modalities(names, mode, load)
    
    # Modalities
    def construct_modalities(self) -> None:
        """Constructs the default modalities for the session."""
        # Use an iterator to construct modalities
        self.modalities.update(
            (name, modality_type(parent_path=self.path, mode=self._mode, **kwargs))  # The key and modality to add
            for name, (modality_type, kwargs) in self.default_modalities.items()  # Iterate over the default modalities
        )
    
    def create_modality(
        self,
        name: str,
        modality: type[Modality] = Modality,
        mode: str | None = None,
        create: bool = True,
        load: bool = False,
        **kwargs: Any,
    ) -> Modality:
        """Creates a new modality for the session.
    
        Args:
            name: The name of the modality.
            modality: The type of modality to create.
            mode: The file mode to set the modality to, defaults to the session's mode.
            create: Determines if the modality will create its contents.
            load: Determines if the modality will load its contents.
            **kwargs: The keyword arguments for the modality.
    
        Returns:
            The newly created modality.
        """
        if name is None:
            name = modality.name
    
        if mode is None:
            mode = self._mode
    
        self.modalities[name] = new_modality = modality(
            name=name,
            parent_path=self.path,
            mode=mode,
            create=create,
            load=load,
            **kwargs,
        )
        return new_modality
    
    def build_modalities(self) -> None:
        """Builds all modalities for the session."""
        for modality in self.modalities.values():
            modality.create(build=True)

    def load_modalities(self, names: Iterable[str] | None = None, mode: str | None = None, load: bool = True) -> None:
        """Loads modalities in this subject.

        Args:
            names: Names of modalities to load. The default None loads all modalities.
            mode: File mode to set the modalities to.
            load: Determines if the modalities will be loaded.
        """
        if mode is None:
            mode = self._mode
        self.modalities.clear()

        # Create path iterator
        if names is None:
            paths = (p for p in self.path.iterdir() if p.is_dir())
        else:
            paths = (self.path / n for n in names)

        # Use an iterator to load modalities
        self.modalities.update((m.name, m) for p in paths if (m := Modality(path=p, mode=mode, load=load)) is not None)
