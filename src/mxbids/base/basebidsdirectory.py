"""basebidsdirectory.py
A base class for mxbids directories.
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
from abc import abstractmethod
from collections.abc import MutableMapping
from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path
from typing import ClassVar, Any
from warnings import warn

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister
from baseobjects.composition import DispatchableComposite

# Local Packages #
from .baseimporter import BaseImporter
from .baseexporter import BaseExporter


# Definitions #
# Classes #
class BaseBIDSDirectory(DispatchableComposite):
    """A base class for mxbids directories.

    Class Attributes:
        default_meta_information: The default meta information about the BIDS directory and how to load it.

    Attributes:
        _path: The path to the BIDS directory.
        _mode: The file mode of the BIDS directory.
        component_types_register: The register of component types.
        name: The name of the BIDS directory.
        importers: The importers of the BIDS directory.
        exporters: The exporters of the BIDS directory.
        _meta_information: The meta information of the BIDS directory.
    """

    # Class Attributes #
    default_meta_information: ClassVar[dict[str, Any]] = {
        "Type": "",
        "Version": "0.1.0",
        "Python": {
            "Module": "",
            "ClassNamespace": "",
            "Class": "",
            "ComponentTypes": {
                # "Name": {"Module": "", "Namespace": "", "Class": "", "Kwargs": {}}
            },
        }
    }

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            **kwargs: The keyword arguments for creating a subclass.
        """
        cls.default_meta_information = deepcopy(cls.default_meta_information)

        super().__init_subclass__(**kwargs)

    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        module = cls._module_ if "_module_" in cls.__dict__ else cls.__module__
        super().register_class(namespace=namespace, name=name)
        cls.default_meta_information["Python"].update(
            ClassNamespace=cls.class_register_namespace,
            Class=cls.class_register_name,
            Module=module[4:] if module.split(".")[0] == "src" else module,
        )

    @classmethod
    def generate_meta_information_path(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
    ) -> Path:
        raise NotImplementedError("This method needs to be implemented to dispatch the class correctly.")

    @classmethod
    def get_class_information(
        cls,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[str, str, str | None]:
        """Gets a class namespace and name from a given set of arguments.

        Args:
            path: The path to the session.
            name: The name of the session.
            parent_path: The path to the parent of the session.
            *args: The arguments to get the namespace and name from.
            **kwargs: The keyword arguments to get the namespace and name from.

        Returns:
            The namespace and name of the class.
        """
        meta_info_path = cls.generate_meta_information_path(path=path, name=name, parent_path=parent_path)
        if not meta_info_path.exists():
            info = cls.default_meta_information["Python"]
        else:
            with meta_info_path.open("r") as file:
                info = json.load(file)["Python"]
        return info["ClassNamespace"], info["Class"], info["Module"]

    # Attributes #
    _path: Path | None = None
    _mode: str = "r"

    component_types_register: ClassNamespaceRegister

    name: str | None = None

    _meta_information: dict[str, Any]

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]]
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]]

    # Properties #
    @property
    def path(self) -> Path | None:
        """The path to the BIDS directory."""
        return self._path

    @path.setter
    def path(self, value: str | Path) -> None:
        if isinstance(value, Path) or value is None:
            self._path = value
        else:
            self._path = Path(value)

    @property
    @abstractmethod
    def directory_name(self) -> str:
        """The directory name of this BIDS Directory object."""

    @property
    @abstractmethod
    def full_name(self) -> str:
        """The full name of this BIDS Directory object."""

    @property
    def meta_information_path(self) -> Path | None:
        """The path to the meta information json file."""
        return None if self._path is None else self._path / f"{self.full_name}_meta.json"

    @property
    def meta_information(self) -> dict[str, Any]:
        """The meta information of this BIDS Directory."""
        return self._meta_information

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str = "r",
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._meta_information = {}

        self.importers = dict(self.importers)
        self.exporters = dict(self.exporters)

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
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
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            path: The path to the BIDS directory.
            name: The name of the BIDS directory.
            parent_path: The path to the parent directory.
            mode: The file mode of the BIDS directory.
            component_kwargs: Keyword arguments for components.
            component_types: Types and arguments for components.
            components: The components of the BIDS directory.
            **kwargs: Additional keyword arguments.
        """
        if name is not None:
            self.name = name

        if path is not None:
            self.path = Path(path)

        if mode is not None:
            self._mode = mode

        if self.meta_information_path is not None and self.meta_information_path.exists():
            self.load_meta_information()

        component_types = self.dispatch_component_types() | (component_types or {})

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def create(self, build: bool = True) -> None:
        """Creates the BIDS directory.

        Args:
            build: Whether to build the directory after creation. Defaults to True.
        """
        self.path.mkdir(exist_ok=True)
        if build:
            self.build()

    def build(self) -> None:
        """Builds the BIDS directory's structure and default files."""
        self.update_meta_information_component_types()
        if not self.meta_information_path.exists():
            self.create_meta_information()

    def load(self, **kwargs: Any) -> None:
        """Loads the BIDS directory.

        Args:
            **kwargs: Additional keyword arguments.
        """
        self.load_meta_information()

    # Components
    def dispatch_component_types(self, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """Dispatches component types using the given arguments.

        Args:
            *args: The arguments to use in dispatching.
            **kwargs: The keyword arguments to use in dispatching.

        Returns:
            The name of the components, their types, and arguments.
        """
        component_types = {}
        meta_info = self._meta_information or self.default_meta_information
        for name, info in meta_info["Python"]["ComponentTypes"].items():
            if (item := self.component_types_register.get_class(info["Namespace"], info["Class"], None)) is None:
                try:
                    import_module(info["Module"])
                except Exception as e:
                    warn(f"Failed to import module {info['Module']} for component {name} with error: {e}")
                else:
                    item = self.component_types_register.get_class(info["Namespace"], info["Class"], None)
            if item is None:
                warn(f"Failed to find component {name} in the component register, skipping.")
            else:
                type_, d_kwargs = item
                component_types[name] = (type_, d_kwargs | info["Kwargs"])
        return component_types

    def update_meta_information_component_types(self, component_kwargs: dict[str, Any] | None = None) -> None:
        """Updates the meta information component types.

        Args:
            component_kwargs: Keyword arguments for components.
        """
        if component_kwargs is None:
            component_kwargs = {}

        for name, component in self.components.items():
            cls = component.__class__
            module = cls.__dict__.get("_module_", cls.__module__)
            if module.split(".")[0] == "src":
                module = module[4:]

            new_component = {
                "Module": module,
                "Namespace": module,
                "Class": cls.__name__,
            }
            if (component := self.meta_information["Python"]["ComponentTypes"].get(name, None)) is None:
                self.meta_information["Python"]["ComponentTypes"][name] = new_component
                new_component["Kwargs"] = component_kwargs.get(name, {})
            else:
                component.update(new_component)
                component["Kwargs"].update(component_kwargs.get(name, {}))

    # Meta Information
    def create_meta_information(self) -> None:
        """Creates meta information file and saves the meta information."""
        if not self._meta_information:
            self._meta_information.update(deepcopy(self.default_meta_information))
        with self.meta_information_path.open(self._mode) as file:
            json.dump(self._meta_information, file)

    def load_meta_information(self) -> dict:
        """Loads the meta information from the file.

        Returns:
            The modality meta information.
        """
        if self._meta_information:
            self._meta_information.clear()

        if self.meta_information_path.exists():
            with self.meta_information_path.open("r") as file:
                self._meta_information.update(json.load(file))

        return self._meta_information

    def save_meta_information(self) -> None:
        """Saves the meta information to the file."""
        with self.meta_information_path.open(self._mode) as file:
            json.dump(self.meta_information, file)

    # Import/Export
    def create_importer(self, name: str, **kwargs: Any) -> BaseImporter:
        """Creates an importer.

        Args:
            name: The name of the importer to create.
            **kwargs: Additional keyword arguments for the importer.

        Returns:
            The created importer.
        """
        importer, d_kwargs = self.importers[name]
        return importer(bids_object=self, **(d_kwargs | kwargs))

    def add_importer(
        self,
        name: str,
        importer: type[BaseImporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        """Adds an importer to this object.

        Args:
            name: The name of the importer to add.
            importer: The importer class to add.
            kwargs: Additional keyword arguments for the importer. Defaults to None.
            overwrite: Determines if an existing importer should be overridden. Defaults to False.
        """
        if name not in self.importers or overwrite:
            self.importers[name] = (importer, kwargs)

    def require_importer(
        self,
        name: str,
        importer: type[BaseImporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> BaseImporter:
        """Gets a specified importer if it exists, creating it if necessary.

        Args:
            name: The name of the importer to get.
            importer: The importer class to get.
            kwargs: Additional keyword arguments for the importer. Defaults to None.
            overwrite: Determines if an existing importer should be overridden. Defaults to False.

        Returns:
            The required importer.
        """
        if kwargs is None:
            kwargs = {}
        importer_, d_kwargs = self.importers.get(name, (None, {}))
        if importer_ is None or overwrite:
            self.importers[name] = (importer, kwargs)
            importer_ = importer

        return importer_(self, **(d_kwargs | kwargs))

    def create_exporter(self, name: str, **kwargs: Any) -> BaseExporter:
        """Creates an exporter.

        Args:
            name: The name of the exporter to create.
            **kwargs: Additional keyword arguments for the exporter.

        Returns:
            BaseExporter: The created exporter.
        """
        exporter, d_kwargs = self.exporters[name]
        return exporter(self, **(d_kwargs | kwargs))

    def add_exporter(
        self,
        name: str,
        exporter: type[BaseExporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        """Adds an exporter to this object.

        Args:
            name: The name of the importer to add.
            exporter: The exporter class to add.
            kwargs: Additional keyword arguments for the importer. Defaults to None.
            overwrite: Determines if an existing importer should be overridden. Defaults to False.
        """
        if name not in self.exporters or overwrite:
            self.exporters[name] = (exporter, kwargs)

    def require_exporter(
        self,
        name: str,
        exporter: type[BaseExporter],
        kwargs: dict[str, Any] | None = None,
        overwrite: bool = False,
    ) -> BaseExporter:
        """Gets a specified exporter if it exists, creating it if necessary.

        Args:
            name: The name of the importer to add.
            exporter: The exporter class to add.
            kwargs: Additional keyword arguments for the importer. Defaults to None.
            overwrite: Determines if an existing importer should be overridden. Defaults to False.

        Returns:
            The required exporter.
        """
        if kwargs is None:
            kwargs = {}
        exporter_, d_kwargs = self.exporters.get(name, (None, {}))
        if exporter_ is None or overwrite:
            self.exporters[name] = (exporter, kwargs)
            exporter_ = exporter

        return exporter_(self, **(d_kwargs | kwargs))
