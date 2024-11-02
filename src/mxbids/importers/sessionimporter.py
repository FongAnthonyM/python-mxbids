"""sessionimporter.py
A BIDS Session Importer.
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
class SessionImporter(BaseImporter):
    """A BIDS Session Importer."""

    # Instance Methods #
    def import_modalities(
        self,
        path: Path,
        inner_maps: list[ImportInnerMap, ...] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Imports modalities from the given path.

        Args:
            path: The root path the files to import.
            inner_maps: The list of maps which map inner objects created from this import and importers for those objects.
            overwrite: Determines if the files should be overridden if they already exist.
            **kwargs: Additional keyword arguments.
        """
        if inner_maps is None:
            inner_maps = self.inner_maps

        for m_name, m_type, i_name, stem, importer, i_overwrite, m_kwargs, i_kwargs in inner_maps:
            modality = self.bids_object.modalities.get(m_name, None)
            if modality is None:
                modality = self.bids_object.create_modality(
                    m_name,
                    m_type,
                    **({"create": True, "build": True} | m_kwargs),
                )

            if importer is None:
                importer, i_kwargs = modality.importers.get(i_name, (None, {}))

            if importer is None:
                importer, i_kwargs = self.default_inner_importer

            over = overwrite if overwrite is not None else i_overwrite
            importer(bids_object=modality, **i_kwargs).execute_import(path.joinpath(stem), overwrite=over)

    def execute_import(
        self,
        path: Path,
        file_maps: bool | list[ImportFileMap, ...] | None = True,
        inner_maps: bool | list[ImportInnerMap, ...] | None = True,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Executes the import process for the session.

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
            self.import_modalities(
                path=path,
                inner_maps=None if isinstance(inner_maps, bool) else inner_maps,
                overwrite=overwrite,
            )
