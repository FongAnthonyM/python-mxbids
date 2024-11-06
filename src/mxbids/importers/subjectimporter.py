"""subjectimporter.py
A BIDS Subject Importer.
"""
from sqlalchemy.orm import object_session

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
class SubjectImporter(BaseImporter):
    """A BIDS Subject Importer."""

    # Instance Methods #
    def import_sessions(
        self,
        path: Path,
        inner_maps: list[ImportInnerMap, ...] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Imports sessions from the given path.

        Args:
            path: The root path the files to import.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            overwrite: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        if inner_maps is None:
            inner_maps = self.inner_maps

        for s_name, s_type, i_name, stem, importer, i_overwrite, s_kwargs, i_kwargs in inner_maps:
            # Correct names
            if s_name[:4] == "ses-":
                s_name = s_name[4:]

            session = self.bids_object.sessions.get(s_name, None)
            if session is None:
                session = self.bids_object.create_session(
                    s_name,
                    s_type,
                    **({"create": True, "build": True} | s_kwargs),
                )

            if importer is None:
                importer, i_kwargs = session.importers.get(i_name, (None, {}))

            if importer is None:
                importer, i_kwargs = self.default_inner_importer

            over = overwrite if overwrite is not None else i_overwrite
            importer(bids_object=session, **i_kwargs).execute_import(path.joinpath(stem), overwrite=over)

    def execute_import(
        self,
        path: Path,
        file_maps: bool | list[ImportFileMap, ...] | None = True,
        inner_maps: bool | list[ImportInnerMap, ...] | None = True,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Executes the import process for the subject.

        Args:
            path: The root path the files to import.
            file_maps: A list of file maps which contain the path information and a callable which imports the file.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            overwrite: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        self.bids_object.create(build=False)
        if file_maps or file_maps is None:
            self.import_files(
                path=path,
                file_maps=None if isinstance(file_maps, bool) else file_maps,
                overwrite=overwrite,
            )
        if inner_maps or inner_maps is None:
            self.import_sessions(
                path=path,
                inner_maps=None if isinstance(inner_maps, bool) else inner_maps,
                overwrite=overwrite,
            )
