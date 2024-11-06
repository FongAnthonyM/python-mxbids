"""functions.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Iterable
from json import dump, load
from pathlib import Path
from shutil import copy2
import subprocess
from warnings import warn

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def strip_json_copy(old_path: Path, new_path: Path, strip: Iterable[str] = ()) -> None:
    """Strips specified fields from a JSON file and writes the cleaned data to a new file.

    Args:
        old_path: The path to the original JSON file.
        new_path: The path to the new JSON file.
        strip: The fields to strip from the JSON data.
    """
    if not old_path.exists():
        warn(f"could not find {old_path}")
        return
    with open(old_path, "r") as f:
        data_orig = load(f)

    data_clean = {key: value for key, value in data_orig.items() if key not in strip}

    with open(new_path, "w") as f:
        dump(data_clean, f)


def command_copy(old_path: Path, new_path: Path, command: str) -> None:
    """Copies a file using a specified command.

    Args:
        old_path: The path to the original file.
        new_path: The path to the new file.
        command: The command to use for copying the file.
    """
    subprocess.run([command, str(old_path), str(new_path)])


def python_copy(old_path: Path, new_path: Path) -> None:
    """Copies a file using the shutil.copy2 function.

    Args:
        old_path: The path to the original file.
        new_path: The path to the new file.
    """
    copy2(old_path, new_path)


__all__ = ["strip_json_copy", "command_copy", "python_copy"]
