"""subjectexporter.py
A class for exporting BIDS subjects.
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

# Third-Party Packages #

# Local Packages #
from ...subjects.subject import Subject
from ..subjectexporter import SubjectExporter
from .sessionbidsexporter import SessionBIDSExporter


# Definitions #
# Classes #
class SubjectBIDSExporter(SubjectExporter):
    """A class for exporting BIDS subjects."""

    # Attributes #
    exporter_name: str = "BIDS"
    export_exclude_names: set[str, ...] = {"meta"}
    default_type: type = (SessionBIDSExporter, {})


# Assign Exporter
Subject.exporters["BIDS"] = (SubjectBIDSExporter, {})
