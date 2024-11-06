"""baseexporter.py
A base class for exporting from the mxbids format.
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
import shutil
from pathlib import Path
from typing import Any

# Third-Party Packages #
from baseobjects import BaseObject

# Local Packages #


# Definitions #
# Classes #
class BaseExporter(BaseObject):
    """A base class for exporting from the mxbids.

    Attributes:
        exporter_name: The name of the exporter.
        export_file_names: The set of file names to export.
        export_exclude_names: The set of file names to exclude from export.
        default_type: The default type for the exporter.
        name_map: A mapping of names.
        type_map: A mapping of types.
        overwrite: Determines if the files should be overridden if they already exist.
        bids_object: The mxbids object to export.

    Args:
        bids_object: The mxbids object to export.
        files_names: The set of file names to export.
        exclude_names: The set of file names to exclude from export.
        name_map: A mapping of names.
        type_map: A mapping of types.
        init: Determines if the object will construct. Defaults to True.
        **kwargs: Additional keyword arguments.
    """

    # Attributes #
    exporter_name: str

    export_file_names: set[str, ...] | None = None
    export_exclude_names: set[str, ...] = {"_meta"}

    default_type: tuple[type["BaseExporter"], dict[str, Any]]
    name_map: dict[str, str] = {}
    type_map: dict[type, (type, dict[str, Any])] = {}
    overwrite: bool = False

    bids_object: Any = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        bids_object: Any = None,
        files_names: set[str, ...] | None = None,
        exclude_names: set[str, ...] | None = None,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        if self.export_file_names is not None:
            self.export_file_names = self.export_file_names.copy()

        self.export_exclude_names = self.export_exclude_names.copy()

        self.name_map = self.name_map.copy()
        self.type_map = self.type_map.copy()

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                bids_object=bids_object,
                files_names=files_names,
                exclude_names=exclude_names,
                name_map=name_map,
                type_map=type_map,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        bids_object: Any = None,
        files_names: set[str, ...] | None = None,
        exclude_names: set[str, ...] | None = None,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            bids_object: The mxbids object to export.
            files_names: The set of file names to export.
            exclude_names: The set of file names to exclude from export.
            name_map: A mapping of names.
            type_map: A mapping of types.
            **kwargs: Additional keyword arguments.
        """
        if bids_object is not None:
            self.bids_object = bids_object

        if files_names is not None:
            if self.export_file_names is None:
                self.export_file_names = files_names.copy()
            else:
                self.export_file_names.update(files_names)

        if exclude_names is not None:
            self.export_exclude_names.update(exclude_names)

        if name_map is not None:
            self.name_map.update(name_map)

        if type_map is not None:
            self.type_map.update(type_map)

        super().construct(**kwargs)

    def export_files(
        self,
        path: Path,
        name: str | None = None,
        files: set[str, ...] | None = None,
        overwrite: bool = False
    ) -> None:
        """Exports files to the specified path.

        Args:
            path: The destination root path for the files to be exported to.
            name: The new name for the exported files. Defaults to None, retaining its name.
            files: The set of file names to export. Defaults to None, exporting all files.
            overwrite: Determines if the files should be overridden if they already exist.
        """
        if files is None:
            files = self.export_file_names

        for old_path in (p for p in self.bids_object.path.iterdir() if p.is_file()):
            old_name = old_path.name
            include = True if files is None else any(n in old_name for n in files)
            exclude = any(n in old_name for n in self.export_exclude_names)
            if include and not exclude:
                new_path = path / (old_name if name is None else old_name.replace(self.bids_object.full_name, name))
                if not new_path.exists() or (overwrite if overwrite is not None else self.overwrite):
                    shutil.copy(old_path, new_path)

    @abstractmethod
    def execute_export(self, path: Path, name: str | None = None, **kwargs: Any) -> None:
        """Abstract method to execute the export process.

        Args:
            path: The destination root path for the exported files.
            name: The new name for the exported files. Defaults to None, retaining its name.
            **kwargs: Additional keyword arguments.
        """
        pass
