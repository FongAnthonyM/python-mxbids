"""importmaps.py
Dataclasses for specifying how to import files into MXBIDS.
"""

# Header #
__package_name__ = "mxbids"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__maintainer__ = "Anthony Fong"
__email__ = ""

__copyright__ = "Copyright 2022, Anthony Fong"
__license__ = "MIT"

__version__ = "0.3.0"
__status__ = "Development Status :: 3 - Alpha"


# Imports #
# Standard Libraries #
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import NamedTuple, Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class ImportFileMap(NamedTuple):
    """A named tuple which maps how to import a file.

    Attributes:
        name: The name of the file to import into.
        extension: The extension of the file to import into.
        paths: Relative paths to the file where each path is checked in order.
        function: The function to use to import the file.
        overwrite: Determines if the file should be overridden if it already exists.
        kwargs: The keyword arguments to pass to the function.
    """

    name: str
    extension: str
    paths: Iterable[Path]
    function: Callable
    overwrite: bool | None = None
    kwargs: dict[str, Any] = {}


class ImportInnerMap(NamedTuple):
    """A named tuple which maps how to import inner BIDS objects.

    Attributes:
        name: The name of the inner BIDS object to import into.
        object_type: The type of the inner BIDS object to import.
        importer_name: The name of the importer to use.
        stem: The stem of the directory to import from.
        importer_type: The type of the importer to use.
        overwrite: Determines if the inner object should be overridden if it already exists.
        object_kwargs: The keyword arguments to pass to the object creation.
        importer_kwargs: The keyword arguments to pass to the importer creation.
    """

    name: str
    object_type: type | None
    importer_name: str
    stem: str
    importer_type: type | None
    overwrite: bool | None = None
    object_kwargs: dict[str, Any] = {}
    importer_kwargs: dict[str, Any] = {}
