""" __init__.py

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
# Local Packages #
from .modalitybidsexporter import ModalityBIDSExporter
from .anatomybidsexporter import AnatomyBIDSExporter
from .ctbidsexporter import CTBIDSExporter
from .ieegbidsexporter import IEEGBIDSExporter
from .sessionbidsexporter import SessionBIDSExporter
from .subjectbidsexporter import SubjectBIDSExporter
from .datasetbidsexporter import DatasetBIDSExporter
