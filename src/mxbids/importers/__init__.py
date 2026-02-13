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
from .file import *
from .modalityimporter import ModalityImporter
from .sessionimporter import SessionImporter
from .subjectimporter import SubjectImporter
from .datasetimporter import DatasetImporter
