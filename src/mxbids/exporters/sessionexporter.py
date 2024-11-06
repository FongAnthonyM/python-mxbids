"""sessionexporter.py
A class for exporting BIDS sessions.
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
from ..base import BaseExporter


# Definitions #
# Classes #
class SessionExporter(BaseExporter):
    """A class for exporting BIDS sessions."""

    # Instance Methods #
    def export_modalities(
        self,
        path: Path,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Exports modalities from the session to the specified path.

        Args:
            path: The root path to export the modalities to.
            name_map: A mapping of original modality names to new names.
            type_map: A mapping of modality types to exporter types.
            overwrite: Determines if existing files will be overwritten.
            **kwargs: Additional keyword arguments.
        """
        if name_map is None:
            name_map = self.name_map

        if type_map is None:
            type_map = self.type_map

        if name_map:
            for modality_name, new_name in name_map.items():
                # Get modality
                modality = self.bids_object.modalities[modality_name]

                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(modality), (None, {}))
                if exporter is not None:
                    exporter(bids_object=modality, **d_kwargs).execute_export(path, name=new_name, overwrite=overwrite)
                else:
                    exporter, d_kwargs = self.default_type
                    m_exporter = modality.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    m_exporter.execute_export(path, name=new_name, overwrite=overwrite)
        else:
            for modality in self.bids_object.modalities.values():
                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(modality), (None, {}))
                if exporter is not None:
                    exporter(bids_object=modality, **d_kwargs).execute_export(path, overwrite=overwrite)
                else:
                    exporter, d_kwargs = self.default_type
                    m_exporter = modality.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    m_exporter.execute_export(path, overwrite=overwrite)

    def execute_export(
        self,
        path: Path,
        name: str | None = None,
        files: bool | set[str, ...] | None = True,
        inner: bool = True,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Executes the export process for the session.

        Args:
            path: The root path to export the session to.
            name: The new name of the exported session. Defaults to None, retaining its name.
            files: A set of files to export or a boolean indicating whether to export files.
            inner: Determines if the inner objects (e.g., modalities) will be exported.
            name_map: A mapping of original names to new name.
            type_map: A mapping of object types to exporter types.
            overwrite: Determines if existing files will be overwritten.
            **kwargs: Additional keyword arguments.
        """
        if name is None:
            name = self.bids_object.full_name.split('_')[1]

        new_path = path / name
        new_path.mkdir(exist_ok=True)
        if files or files is None:
            new_name = f"{path.parts[-1]}_{name}"
            self.export_files(
                path=new_path,
                name=new_name,
                files=None if isinstance(files, bool) else files,
                overwrite=overwrite,
            )
        if inner:
            self.export_modalities(path=new_path, name_map=name_map, type_map=type_map, overwrite=overwrite)
