"""subjectexporter.py
A class for exporting BIDS subjects.
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
