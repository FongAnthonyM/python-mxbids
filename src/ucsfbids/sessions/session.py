"""session.py
A base class which defines a Session and dispatches a specific Session subclass based on meta information.
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
    """A base class which defines a Session and dispatches a specific Session subclass based on meta information.

    Class Attributes:
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        register: A register of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the register.
        meta_information: The default meta information about the session.

    Attributes:
        _path: The path to session.
        _is_open: Determines if this session and its contents are open.
        _mode: The file mode of this session.
        meta_info: The meta information that describes this session.
        name: The name of this session.
        parent_name: The name of the parent subject of this session.

    Args:
        path: The path to the session's directory.
        name: The name of the session.
        parent_path: The parent path of this session.
        mode: The file mode to set this session to.
        create: Determines if this session will be created if it does not exist.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "ucsfbids.sessions"

    class_register: ClassVar[dict[str, dict[str, type]]] = {}
    class_registration: ClassVar[bool] = True
    class_register_namespace: ClassVar[str | None] = "ucsfbids"
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
        """Constructs this object.

        Args:
            path: The path to the subject's directory.
            name: The ID name of the subject.
            parent_path: The parent path of this subject.
            mode: The file mode to set this subject to.
            create: Determines if this subject will be created if it does not exist.
            load: Determines if the sessions will be loaded from the subject's directory.
            kwargs: The keyword arguments for inheritance if any.
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

        # Construct Parent #
        super().construct(**kwargs)

        # Create
        if self.path is not None and not self.path.exists() and create:
            self.create(build=build)

    def build(self) -> None:
        super().build()
        self.build_modalities()

    def load(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        super().load()
        self.load_modalities(names, mode, load)

    # Modalities
    def construct_modalities(self) -> None:
        # Use an iterator to construct modalities
        self.modalities.update(
            (name, modality_type(parent_path=self.path, mode=self._mode, **kwargs))  # The key and modality to add
            for name, (modality_type, kwargs) in self.default_modalities.items()  # Iterate over the default modalities
        )

    def build_modalities(self) -> None:
        for modality in self.modalities.values():
            modality.create()

    def load_modalities(self, names: Iterable[str] | None = None, mode: str | None = None, load: bool = True) -> None:
        """Loads all modalities in this session."""
        m = self._mode if mode is None else mode
        self.modalities.clear()

        # Use an iterator to load modalities
        self.modalities.update(
            (s.name, s)  # The key and modality to add
            for p in self.path.iterdir()  # Iterate over the path's contents
            # Check if the path is a directory and the name is in the names list
            if p.is_dir() and (names is None or any(n in p.stem for n in names)) and
            # Create a modality and check if it is valid
            (s := Modality(path=p, mode=m, load=load)) is not None
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
        """Create a new session for this subject with a given session type and arguments.

        Args:
            modality: The type of session to create.
            name: The name of the new session, defaults to the latest generated name.
            mode: The file mode to set the session to, defaults to the subject's mode.
            create: Determines if the session will create its contents.
            load: Determines if the sessions will be loaded from the subject's directory.
            **kwargs: The keyword arguments for the session.

        Returns:
            The newly created session.
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
