"""datasetimporter.py
A BIDS Dataset Importer.
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
from pathlib import Path
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseImporter, ImportFileMap, ImportInnerMap


# Definitions #
# Classes #
class DatasetImporter(BaseImporter):
    """A BIDS Dataset Importer."""

    # Instance Methods #
    def import_subjects(
        self,
        path: Path,
        inner_maps: list[ImportInnerMap, ...] | None = None,
        override: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Imports subjects from the given path.

        Args:
            path: The root path the files to import.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            override: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        if inner_maps is None:
            inner_maps = self.inner_maps

        for s_name, s_type, i_name, stem, importer, i_override, s_kwargs, i_kwargs in inner_maps:
            # Correct names
            if s_name[:4] == "sub-":
                s_name = s_name[4:]

            subject = self.bids_object.subjects.get(s_name, None)
            if subject is None:
                subject = self.bids_object.create_subject(
                    s_name,
                    s_type,
                    **({"create": True, "build": True} | s_kwargs),
                )

            if importer is None:
                importer, i_kwargs = subject.importers.get(i_name, (None, {}))

            if importer is None:
                importer, i_kwargs = self.default_inner_importer

            over = override if override is not None else i_override
            importer(bids_object=subject, **i_kwargs).execute_import(path.joinpath(stem), override=over)

    def execute_import(
        self,
        path: Path,
        file_maps: bool | list[ImportFileMap, ...] | None = True,
        inner_maps: bool | list[ImportInnerMap, ...] | None = True,
        override: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Executes the import process for the dataset.

        Args:
            path: The root path the files to import.
            file_maps: A list of file maps which contain the path information and a callable which imports the file.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            override: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        self.bids_object.create(build=False)
        if file_maps or file_maps is None:
            self.import_files(
                path=path,
                file_maps=None if isinstance(file_maps, bool) else file_maps,
                override=override,
            )
        if inner_maps or inner_maps is None:
            self.import_subjects(
                path=path,
                inner_maps=None if isinstance(inner_maps, bool) else inner_maps,
                override=override,
            )
