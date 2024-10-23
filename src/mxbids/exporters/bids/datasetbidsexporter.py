"""datasetbidsexporter.py
A class for exporting BIDS datasets.
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
from ...datasets import Dataset
from ..datasetexporter import DatasetExporter
from .subjectbidsexporter import SubjectBIDSExporter


# Definitions #
# Classes #
class DatasetBIDSExporter(DatasetExporter):
    """A class for exporting BIDS datasets."""

    # Attributes #
    exporter_name: str = "BIDS"
    export_exclude_names: set[str, ...] = {"meta"}
    default_type: type = (SubjectBIDSExporter, {})


# Assign Exporter
Dataset.exporters["BIDS"] = (DatasetBIDSExporter, {})
