"""modalityexporter.py
A class for exporting BIDS modalities.
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
class ModalityExporter(BaseExporter):
    """A class for exporting BIDS modalities."""

    # Instance Methods #
    def execute_export(
        self,
        path: Path,
        name: str | None = None,
        files: bool | set[str, ...] | None = True,
        **kwargs: Any,
    ) -> None:
        """Executes the export process for the modality.

        Args:
            path: The root path to export the modality to.
            name: The new name of the exported modality. Defaults to None, retaining the original name.
            files: A set of files to export or a boolean indicating whether to export files.
            **kwargs: Additional keyword arguments.
        """
        if name is None:
            name = self.bids_object.full_name

        new_path = path / f"{self.bids_object.name}"
        new_path.mkdir(exist_ok=True)
        if files or files is None:
            self.export_files(path=new_path, name=name, files=files)