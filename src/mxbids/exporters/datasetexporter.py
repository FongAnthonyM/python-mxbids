"""datasetexporter.py
A class for exporting BIDS datasets.
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
import traceback
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..base import BaseExporter


# Definitions #
# Classes #
class DatasetExporter(BaseExporter):
    """A class for exporting BIDS datasets."""

    # Instance Methods #
    def export_subjects(
        self,
        path: Path,
        name_map: dict[str, str] | None = None,
        type_map: dict[type, type] | None = None,
        overwrite: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Exports subjects from the dataset to the specified path.

        Args:
            path: The root path to export the subjects to.
            name_map: A mapping of original subject names to new names.
            type_map: A mapping of subject types to exporter types.
            overwrite: Determines if existing files will be overwritten.
            **kwargs: Additional keyword arguments.
        """
        if name_map is None:
            name_map = self.name_map

        if type_map is None:
            type_map = self.type_map

        if name_map:
            for subject_name, new_name in name_map.items():
                # Correct names
                if subject_name[:4] == "sub-":
                    subject_name = subject_name[4:]
                if new_name[:4] != "sub-":
                    new_name = f"sub-{new_name}"

                # Get subject
                subject = self.bids_object.subjects[subject_name]

                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(subject), (None, {}))
                if exporter is not None:
                    exporter(bids_object=subject, **d_kwargs).execute_export(path, name=new_name, overwrite=overwrite)
                else:
                    exporter, d_kwargs = self.default_type
                    s_exporter = subject.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    try:
                        s_exporter.execute_export(path, name=new_name, overwrite=overwrite)
                    except Exception as e:
                        print(f"There was an error with {subject.name}")
                        print(f"{e}")
                        print(f"{traceback.print_exc()}")
        else:
            for subject in self.bids_object.subjects.values():
                # Export using correct exporter type
                exporter, d_kwargs = type_map.get(type(subject), (None, {}))
                if exporter is not None:
                    exporter(bids_object=subject, **d_kwargs).execute_export(path, overwrite=overwrite)
                else:
                    exporter, d_kwargs = self.default_type
                    s_exporter = subject.require_exporter(self.exporter_name, exporter, **d_kwargs)
                    try:
                        s_exporter.execute_export(path, overwrite=overwrite)
                    except Exception as e:
                        print(f"There was an error with {subject.name}")
                        print(f"{e}")
                        print(f"{traceback.print_exc()}")

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
        """Executes the export process for the dataset.

        Args:
            path: The root path to export the dataset to.
            name: The new name of the exported dataset. Defaults to None, retaining its name.
            files: A set of files to export or a boolean indicating whether to export files.
            inner: Determines if the inner objects (e.g., subjects) will be exported.
            name_map: A mapping of original names to new names.
            type_map: A mapping of object types to exporter types.
            overwrite: Determines if existing files will be overwritten.
            **kwargs: Additional keyword arguments.
        """
        if name is None:
            name = self.bids_object.full_name

        new_path = path if name is None else path / name
        new_path.mkdir(exist_ok=True)
        if files or files is None:
            self.export_files(
                path=new_path,
                name=name,
                files=None if isinstance(files, bool) else files,
                overwrite=overwrite,
            )
        if inner:
            self.export_subjects(path=new_path, name_map=name_map, type_map=type_map, overwrite=overwrite)
