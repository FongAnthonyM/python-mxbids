"""ieegcdfscomponent.py
A component for the IEEG modality which implements access a CDFS.
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
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects.composition import BaseComponent
from cdfs import BaseCDFS

# Local Packages #


# Definitions #
# Classes #
class IEEGCDFSComponent(BaseComponent):
    """A component for the IEEG modality which implements access a CDFS.

    Attributes:
        _module_: The module name for this class.
        cdfs_type: The type of the CDFS to access.
        cdfs: The CDFS instance.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "ucsfbids.cdfsbids"

    # Attributes #
    cdfs_type: type[BaseCDFS] = BaseCDFS
    cdfs: BaseCDFS | None = None

    # Instance Methods #
    # Construction/Destruction
    def construct_cdfs(self, file_name: str | None = None, create: bool = False, **kwargs: Any) -> BaseCDFS:
        """Creates or loads the CDFS of this modality.

        Args:
            file_name: The name of the contents file of the CDFS. If None, the name will be generated from modality.
            create: Determines if the CDFS will be created. Defaults to False.
            **kwargs: The keyword arguments for creating the CDFS.

        Returns:
            The CDFS of this modality.
        """
        if file_name is None:
            file_name = self.generate_contents_file_name()

        composite = self._composite()
        self.cdfs = cdfs = self.cdfs_type(
            path=composite.path,
            name=composite.full_name,
            mode=composite._mode,
            create=create,
            contents_name=file_name,
            **kwargs,
        )
        return cdfs

    def build(self) -> None:
        """Builds the CDFS for this modality."""
        self.construct_cdfs(create=True, build=True)

    def load(self) -> None:
        """Loads the CDFS for this modality."""
        self.construct_cdfs(open_=True, create=False)

    # Content File
    def generate_contents_file_name(self) -> str:
        """Generates a name for the contents file from the subject and session name.

        Returns:
            The name of the contents file.
        """
        return f"{self._composite().full_name}_contents.sqlite3"
