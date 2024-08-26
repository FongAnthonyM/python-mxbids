"""subject.py

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
from ..sessions import Session


# Definitions #
# Classes #
class Subject(BaseBIDSDirectory):
    """A subject in the UCSF BIDS format.

    Attributes:
        _path: The path to subject.
        _is_open: Determines if this subject and its contents are open.
        _mode: The file mode of this subject.
        name: The name of this subject.
        sessions: The session of the subject.

    Args:
        path: The path to the subject's directory.
        name: The ID name of the subject.
        parent_path: The parent path of this subject.
        mode: The file mode to set this subject to.
        create: Determines if this subject will be created if it does not exist.
        load: Determines if the sessions will be loaded from the subject's directory.
        init: Determines if this object will construct.
        kwargs: The keyword arguments for inheritance if any.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "ucsfbids.subjects"

    class_register: ClassVar[dict[str, dict[str, type]]] = {}
    class_registration: ClassVar[bool] = True
    class_register_namespace: ClassVar[str | None] = "ucsfbids"
    default_meta_information: ClassVar[dict[str, Any]] = deepcopy(BaseBIDSDirectory.default_meta_information) | {
        "Type": "Subject",
    }

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
            path = (parent_path if isinstance(parent_path, Path) else Path(parent_path)) / f"sub-{name}"
        else:
            raise ValueError("Either path or (parent_path and name) must be given to dispatch class.")

        return path / f"sub-{name}_meta.json"

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    session_prefix: str = "S"
    session_digits: int = 4

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    sessions: dict[str, Session]

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Subject."""
        return f"sub-{self.name}"

    @property
    def full_name(self) -> str:
        """The full name of this Subject."""
        return f"sub-{self.name}"

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
        sessions_to_load: list[str] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.sessions: dict[str, Session] = {}

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
                sessions_to_load=sessions_to_load,
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
        sessions_to_load: list[str] | None = None,
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

        # Load
        if self.path is not None and self.path.exists() and load:
            self.load(sessions_to_load)

        # Construct Parent #
        super().construct(**kwargs)

        # Create
        if self.path is not None and not self.path.exists() and create:
            self.create(build=build)

    def build(self) -> None:
        super().build()
        self.build_sessions()

    def load(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        super().load()
        self.load_sessions(names, mode, load)

    # Session
    def build_sessions(self) -> None:
        for session in self.sessions.values():
            session.create()

    def load_sessions(self, names: Iterable[str] | None = None, mode: str | None = None, load: bool = True) -> None:
        """Loads all sessions in this subject."""
        m = self._mode if mode is None else mode
        self.sessions.clear()

        # Use an iterator to load sessions
        self.sessions.update(
            (s.name, s)  # The key and session to add
            for p in self.path.iterdir()  # Iterate over the path's contents
            # Check if the path is a directory and the name is in the names list
            if p.is_dir() and (names is None or any(n in p.stem for n in names)) and
            # Create a session and check if it is valid
            (s := Session(path=p, mode=m, load=load)) is not None
        )

    def generate_latest_session_name(self, prefix: str | None = None, digits: int | None = None) -> str:
        """Generates a subject name for a new latest subject.

        Returns:
            The name of the latest session to create.
        """
        if prefix is None:
            prefix = self.session_prefix
        if digits is None:
            digits = self.session_digits
        return f"{prefix}{len(self.sessions):0{digits}d}"

    def create_session(
        self,
        name: str | None = None,
        session: type[Session] = Session,
        mode: str | None = None,
        create: bool = True,
        load: bool = False,
        **kwargs: Any,
    ) -> Session:
        """Create a new session for this subject with a given session type and arguments.

        Args:
            session: The type of session to create.
            name: The name of the new session, defaults to the latest generated name.
            mode: The file mode to set the session to, defaults to the subject's mode.
            create: Determines if the session will create its contents.
            load: Determines if the sessions will be loaded from the subject's directory.
            **kwargs: The keyword arguments for the session.

        Returns:
            The newly created session.
        """
        if name is None:
            name = self.generate_latest_session_name()

        if mode is None:
            mode = self._mode

        self.sessions[name] = new_session = session(
            name=name,
            parent_path=self.path,
            mode=mode,
            create=create,
            load=load,
            **kwargs,
        )
        return new_session
