"""dataset.py
A BIDS Dataset.
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
from collections.abc import Iterable, MutableMapping
from collections import ChainMap
from copy import deepcopy
from pathlib import Path
import json
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister
import pandas as pd

# Local Packages #
from ..base import BaseBIDSDirectory, BaseImporter, BaseExporter
from ..subjects import Subject


# Definitions #
# Classes #
class Dataset(BaseBIDSDirectory):
    """A BIDS Dataset.

    Class Attributes:
        _module_: The module name to use in class dispatching.
        class_register: The class register.
        class_registration: Determines if this class and its subclasses will be registered.
        class_register_namespace: The namespace of this class for class registration.
        default_meta_information: Default metadata information for the dataset.
        default_description: Default description for the dataset.

    Attributes:
        component_types_register: Register for component types.
        subject_prefix: Prefix for subject IDs.
        subject_digits: Number of digits for subject IDs.
        importers: Importers for the dataset.
        exporters: Exporters for the dataset.
        _description: Description of the dataset.
        _participant_fields: Fields for participants.
        participants: DataFrame containing participant information.
        subjects: Dictionary of subjects in the dataset.

    Args:
        path: The path to the dataset's directory.
        name: The name of the dataset.
        parent_path: The parent path of this dataset.
        mode: The file mode to set this dataset to.
        create: Determines if the dataset will be created if it does not exist.
        build: Determines if the dataset will be built after creation.
        load: Determines if the dataset will be load.
        load_subjects: Determines if the subjects will be loaded can provide a list of subjects to load.
        load_sessions: Determines if the sessions will be loaded can provide a list of sessions to load.
        load_modalities: Determines if the modalities will be loaded can provide a list of modalities to load.
        init: Determines if the object will construct. Defaults to True.
        **kwargs: Additional keyword arguments.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.datasets"

    class_register: ClassVar[dict[str, dict[str, type]]] = {}
    class_registration: ClassVar[bool] = True
    class_register_namespace: ClassVar[str | None] = "mxbids"
    default_meta_information: ClassVar[dict[str, Any]] = deepcopy(BaseBIDSDirectory.default_meta_information) | {
        "Type": "Dataset",
    }
    default_description: ClassVar[dict[str, Any]] = {
        "Name": "Default name, should be updated",
        "BIDSVersion": "1.6.0",
        "DatasetType": "raw",
    }
    default_participant_fields: ClassVar[dict[str, Any]] = {
        "participant_id": {
            "Description": "A unique identifier for the participant.",
        },
    }

    # Class Methods #
    @classmethod
    def generate_meta_information_path(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
    ) -> Path:
        """Generates the path for the meta information file.

        Args:
            path: The path to the dataset.
            name: The name of the dataset.
            parent_path: The path to the parent of the dataset.

        Returns:
            Path: The path to the meta information file.
        """
        if path is not None:
            if not isinstance(path, Path):
                path = Path(path)
        else:
            raise ValueError("path must be given to dispatch class.")

        return path / f"dataset_meta.json"

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    subject_prefix: str = "S"
    subject_digits: int = 4

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = ChainMap()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = ChainMap()

    _description: dict[str, Any] | None = None

    _participant_fields: dict[str, Any] | None = None
    participants: pd.DataFrame | None = None

    subjects: dict[str, Subject]

    # Properties #
    @property
    def directory_name(self) -> str:
        """The directory name of this Dataset."""
        return self.path.stem

    @property
    def full_name(self) -> str:
        """The full name of this Dataset."""
        return self.name

    @property
    def meta_information_path(self) -> Path:
        """The path to the meta information json file."""
        return self._path / f"dataset_meta.json"

    @property
    def description_path(self) -> Path:
        """The path to the description json file."""
        return self._path / f"dataset_description.json"

    @property
    def description(self) -> dict[str, Any]:
        """The description of the dataset."""
        if self._description is None:
            return self.default_description.copy()
        else:
            return self._description

    @property
    def participant_fields_path(self) -> Path:
        """The path to the participant json file."""
        return self._path / f"participants.json"

    @property
    def participant_fields(self) -> dict[str, Any]:
        """The participant fields of the dataset."""
        if self._participant_fields is None:
            return self.default_participant_fields.copy()
        else:
            return self._participant_fields

    @property
    def participants_path(self) -> Path:
        """The path to the participant tsv file."""
        return self._path / f"participants.tsv"

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
        load_subjects: bool | Iterable[str] = False,
        load_sessions: bool | Iterable[str] = False,
        load_modalities: bool | Iterable[str] = True,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.subjects = {}

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
                load_subjects=load_subjects,
                load_sessions=load_sessions,
                load_modalities=load_modalities,
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
        load_subjects: bool | Iterable[str] = False,
        load_sessions: bool | Iterable[str] = False,
        load_modalities: bool | Iterable[str] = True,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the dataset's directory.
            name: The name of the dataset.
            parent_path: The parent path of this dataset.
            mode: The file mode to set this dataset to.
            create: Determines if the dataset will be created if it does not exist.
            build: Determines if the dataset will be built after creation.
            load: Determines if the dataset will be load.
            load_subjects: Determines if the subjects will be loaded, can provide a list of subjects to load.
            load_sessions: Determines if the sessions will be loaded, can provide a list of sessions to load.
            load_modalities: Determines if the modalities will be loaded, can provide a list of modalities to load.
            kwargs: The keyword arguments for inheritance if any.
        """
        if name is not None:
            self.name = name

        if path is not None:
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        if parent_path is not None and name is not None:
            if isinstance(parent_path, str):
                parent_path = Path(parent_path)
            self.path = parent_path / name

        # Load
        if self.path is not None and self.path.exists():
            if load:
                self.load()

            if load_subjects:
                names = None if isinstance(load_subjects, bool) else load_subjects
                self.load_subjects(names=names, load_sessions=load_sessions, load_modalities=load_modalities)

        # Construct Parent #
        super().construct(**kwargs)

        # Create
        if self.path is not None and create:
            self.create(build=build)

    def build(self) -> None:
        """Builds the dataset."""
        super().build()
        if not self.description_path.exists():
            self.create_description()

    def load(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        **kwargs: Any,
    ) -> None:
        """Loads the dataset.

        Args:
            names: Names of subjects to load.
            mode: File mode to set the subjects to.
            load: Determines if the subjects will be loaded.
            kwargs: Additional keyword arguments.
        """
        super().load()
        if self.description_path.exists():
            self.load_description()
        if self.participant_fields_path.exists():
            self.load_participant_fields()
        if self.participants_path.exists():
            self.load_participants()

    # Description
    def create_description(self) -> None:
        """Creates description file and saves the description."""
        if self._description is None:
            self._description = deepcopy(self.default_description)
        self._description["Name"] = self.name
        with self.description_path.open(self._mode) as file:
            json.dump(self._description, file)

    def load_description(self) -> dict:
        """Loads the description from the file.

        Returns:
            The dataset description.
        """
        if self._description is None:
            self._description = {}
        else:
            self._description.clear()

        with self.description_path.open("r") as file:
            self._description.update(json.load(file))

        self.name = self._description["Name"]

        return self._description

    def save_description(self) -> None:
        """Saves the description to the file."""
        self.description["Name"] = self.name
        with self.description_path.open(self._mode) as file:
            json.dump(self.description, file)

    # Participant Fields
    def create_participant_fields(self) -> None:
        """Creates participant fields file and saves the participant_fields."""
        if self._participant_fields is None:
            self._participant_fields = deepcopy(self.default_participant_fields)
        with self.participant_fields_path.open(self._mode) as file:
            json.dump(self._participant_fields, file)

    def load_participant_fields(self) -> dict:
        """Loads the participant fields from the file.

        Returns:
            The dataset participant fields.
        """
        if self._participant_fields is None:
            self._participant_fields = {}
        else:
            self._participant_fields.clear()

        with self.participant_fields_path.open("r") as file:
            self._participant_fields.update(json.load(file))

        return self._participant_fields

    def save_participant_fields(self) -> None:
        """Saves the participant_fields to the file."""
        with self.participant_fields_path.open(self._mode) as file:
            json.dump(self.participant_fields, file)

    # Participants
    def create_participants(self) -> None:
        """Creates participants file and saves the participants."""
        if self.participants is None:
            self.participants = pd.DataFrame(columns=tuple(self.participant_fields.keys()))

        self.participants.to_csv(self.participants_path, mode=self._mode, sep="\t")

    def load_participants(self) -> pd.DataFrame:
        """Loads the participant information from the file.

        Returns:
            The participant information.
        """
        self.participants = participants = pd.read_csv(self.participants_path, sep="\t")
        return participants

    def save_participants(self) -> None:
        """Saves the participants to the file."""
        self.participants.to_csv(self.participants_path, mode=self._mode, sep="\t")

    # Subjects
    def generate_latest_subject_name(self, prefix: str | None = None, digits: int | None = None) -> str:
        """Generates a subject name for a new latest subject.

        Args:
            prefix: Prefix for the subject name.
            digits: Number of digits for the subject name.

        Returns:
            The name of the latest subject to create.
        """
        if prefix is None:
            prefix = self.subject_prefix
        if digits is None:
            digits = self.subject_digits
        return f"{prefix}{len(self.subjects):0{digits}d}"

    def create_subject(
        self,
        name: str | None = None,
        subject: type[Subject] = Subject,
        mode: str | None = None,
        create: bool = True,
        load: bool = False,
        **kwargs: Any,
    ) -> Subject:
        """Create a new subject for this dataset with a given subject type and arguments.

        Args:
            name: The name of the new subject, defaults to the latest generated name.
            subject: The type of subject to create.
            mode: The file mode to set the subject to, defaults to the dataset's mode.
            create: Determines if the subject will create its contents.
            load: Determines if the subject will load its contents.
            kwargs: The keyword arguments for the subject.

        Returns:
            The newly created subject.
        """
        if name is None:
            name = self.generate_latest_subject_name()

        if mode is None:
            mode = self._mode

        self.subjects[name] = new_subject = subject(
            name=name,
            parent_path=self.path,
            mode=mode,
            create=create,
            load=load,
            **kwargs,
        )
        return new_subject

    def load_subjects(
        self,
        names: Iterable[str] | None = None,
        mode: str | None = None,
        load: bool = True,
        clear: bool = True,
        **kwargs: Any,
    ) -> None:
        """Loads subjects in this dataset.

        Args:
            names: Names of subjects to load. The default None loads all subjects.
            mode: File mode to set the subjects to.
            load: Determines if the subjects will be loaded.
            clear: Determines if the subjects will be cleared before loading.
            kwargs: Keyword arguments for the subjects.
        """
        if mode is None:
            mode = self._mode

        if clear:
            self.subjects.clear()

        # Create path iterator
        if names is None:
            names_ = self.path.iterdir()
        else:
            names_ = (self.path / (n if n[:4] == "sub-" else f"sub-{n}") for n in names)

        paths = (p for p in names_ if p.is_dir())

        # Use an iterator to load subjects
        kwargs_ = {"mode": mode, "load": load} | kwargs
        self.subjects.update((s.name, s) for p in paths if (s := Subject(path=p, **kwargs_)) is not None)

    def print_children(self, indent: int = 0) -> None:
        """Prints the children of the dataset."""
        print(f"{' ' * indent}Dataset: {self.name}")
        for s in self.subjects.values():
            s.print_children(indent=indent + 4)
