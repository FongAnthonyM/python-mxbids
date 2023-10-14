""" __init__.py

"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .modalitybidsimporter import ModalityBIDSImporter
from .base import AnatomyBIDSImporter
from .base import CTBIDSImporter 
from .base import IEEGBIDSImporter 
