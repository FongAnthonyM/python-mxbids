"""ieegbidsexporter.py
A class for exporting BIDS iEEG data.
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
from ...modalities import IEEG
from .modalitybidsexporter import ModalityBIDSExporter


# Definitions #
# Classes #
class IEEGBIDSExporter(ModalityBIDSExporter):
    """A class for exporting BIDS iEEG data."""

    # Attributes #
    export_file_names: set[str, ...] = {"ieeg", "coordsystem", "electrodes", "channels", "photo"}
    export_exclude_names: set[str, ...] = {"ieeg_meta"}


# Assign Exporter
IEEG.exporters["BIDS"] = (IEEGBIDSExporter, {})
