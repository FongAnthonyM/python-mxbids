"""modalityimporter.py
A BIDS Modality Importer.
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

# Third-Party Packages #

# Local Packages #
from ..base import BaseImporter


# Definitions #
# Classes #
class ModalityImporter(BaseImporter):
    """A BIDS Modality Importer."""

    # Instance Methods #
    def execute_import(self, path: Path, file_maps: bool | list[tuple] | None = True) -> None:
        """Executes the import process for the modality.

        Args:
            path: The root path the files to import.
            file_maps: A list of file maps which contain the path information and a callable which imports the file.
        """
        self.bids_object.create(build=False)
        if file_maps or file_maps is None:
            self.import_files(path=path, file_maps=file_maps)
