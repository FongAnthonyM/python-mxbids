"""baseimporter.py
A base class for importing files to mxbids.
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
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any
from warnings import warn

# Third-Party Packages #
from baseobjects import BaseObject

# Local Packages #
from .importmaps import ImportFileMap, ImportInnerMap


# Definitions #
# Classes #
class BaseImporter(BaseObject):
    """A base class for importing files to mxbids.

    Attributes:
        importer_name: The name of the importer.
        default_inner_importer: The default importer for inner objects if an importer is not given.
        file_maps: A list of file maps which contain the path information and a callable which imports the file.
        inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
        bids_object: The mxbids object to import to.

    Args:
        bids_object: The mxbids object to import to.
        file_maps: A list of file maps which contain the path information and a callable which imports the file.
        inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
        overwrite: Determines if the files should be overridden if they already exist.
        init: Determines if the object will construct. Defaults to True.
        **kwargs: Additional keyword arguments.
    """

    # Attributes #
    importer_name: str

    default_inner_importer: tuple[type["BaseImporter"], dict[str, Any]]
    file_maps: list[ImportFileMap, ...] = []
    inner_maps: list[ImportInnerMap, ...] = []
    overwrite: bool = False

    bids_object: Any = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        bids_object: Any = None,
        file_maps: list[ImportFileMap, ...] | None = None,
        inner_maps: list[ImportInnerMap, ...] | None = None,
        overwrite: bool | None = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.file_maps = self.file_maps.copy()
        self.inner_maps = self.inner_maps.copy()

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                bids_object=bids_object,
                file_maps=file_maps,
                inner_maps=inner_maps,
                overwrite=overwrite,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        bids_object: Any = None,
        file_maps: list[ImportFileMap, ...] | None = None,
        inner_maps: list[ImportInnerMap, ...] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            bids_object: The mxbids object to import to.
            file_maps: A list of file maps which contain the path information and a callable which imports the file.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            overwrite: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        if bids_object is not None:
            self.bids_object = bids_object

        if file_maps is not None:
            self.file_maps.clear()
            self.file_maps.extend(file_maps)

        if inner_maps is not None:
            self.inner_maps.clear()
            self.inner_maps.extend(inner_maps)

        if overwrite is not None:
            self.overwrite = overwrite

        super().construct(**kwargs)

    def import_files(
        self,
        path: Path,
        file_maps: list[ImportFileMap, ...] | None = None,
        overwrite: bool | None = None,
    ) -> None:
        """Imports files from the specified path.

        Args:
            path: The root path of the files to import.
            file_maps: A list of file maps which contain the path information and a callable which imports the file.
            overwrite: Determines if the files should be overridden if they already exist.
        """
        if file_maps is None:
            file_maps = self.file_maps

        for suffix, extension, relative_paths, import_call, i_overwrite, i_kwargs in file_maps:
            new_path = self.bids_object.path / f"{self.bids_object.full_name}_{suffix}{extension}"
            over = overwrite if overwrite is not None else (i_overwrite if i_overwrite is not None else self.overwrite)
            if not new_path.exists() or over:
                for relative_path in relative_paths:
                    if relative_path is not None:
                        inner_path = path / relative_path
                        if not inner_path.exists():
                            continue
                    else:
                        inner_path = None
                    try:
                        import_call(inner_path, new_path, **i_kwargs)
                    except Exception as e:
                        warn(f"Failed to BIDS import {inner_path} to {new_path} with error: {e}", RuntimeWarning)
                    else:
                        break

    @abstractmethod
    def execute_import(self, path: Path, overwrite: bool | None = None, **kwargs: Any) -> None:
        """Abstract method to execute the import process.

        Args:
            path: The root path the files to import.
            overwrite: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
