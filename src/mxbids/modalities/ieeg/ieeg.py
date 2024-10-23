"""ieeg.py
A BIDS IEEG Modality.
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
from collections.abc import MutableMapping
from copy import deepcopy
import json
from pathlib import Path
from typing import ClassVar, Any

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister
import pandas as pd

# Local Packages #
from ...base import BaseImporter, BaseExporter
from ..modality import Modality


# Definitions #
# Classes #
class IEEG(Modality):
    """A BIDS IEEG Modality.

    Class Attributes:
        _module_: The module name for this class.
        class_register_namespace: The namespace for class registration.
        default_ieeg_metadata: Default IEEG metadata.
        default_coordinate_system: Default coordinate system.

    Attributes:
        component_types_register: Register for component types.
        name: The name of the modality.
        _ieeg_metadata: The IEEG metadata.
        _coordinate_system: The coordinate system.
        electrode_columns: List of electrode column names.
        electrodes: DataFrame containing electrode information.
        channel_columns: List of channel column names.
        channels: DataFrame containing channel information.
        event_columns: List of event column names.
        events: DataFrame containing event information.
        importers: Mapping of importers.
        exporters: Mapping of exporters.

    Args:
        path: The path to the modality's directory.
        name: The name of the modality.
        parent_path: The path to the parent directory.
        mode: The file mode to set for the modality.
        create: Determines if this modality will be created if it does not exist.
        build: Determines if the directory will be built after creation.
        load: Determines if the modality will load.
        init: Determines if this object will construct.
        **kwargs: Additional keyword arguments.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = "mxbids.modalities"
    class_register_namespace: ClassVar[str | None] = "mxbids.ieeg"

    default_ieeg_metadata: ClassVar[dict[str, Any]] = {}
    default_coordinate_system: ClassVar[dict[str, Any]] = {"iEEGCoordinateSystem": "ACPC", "iEEGCoordinateUnits": "mm"}

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    name: str = "ieeg"

    _ieeg_metadata: dict[str, Any] | None = None

    _coordinate_system: dict[str, Any] | None = None

    electrode_columns: list[str] = [
        "name",
        "x",
        "y",
        "z",
        "size",
        "material",
        "manufacturer",
        "group",
        "hemisphere",
        "type",
        "impedance",
        "dimension",
    ]
    electrodes: pd.DataFrame | None = None

    channel_columns: list[str] = [
        "name",
        "type",
        "units",
        "low_cutoff",
        "high_cutoff",
    ]
    channels: pd.DataFrame | None = None

    event_columns: list[str] = [
        "onset",
        "duration",
        "electrical_stimulation_type",
        "electrical_stimulation_site",
        "electrical_stimulation_current",
    ]
    events: pd.DataFrame | None = None

    importers: MutableMapping[str, tuple[type[BaseImporter], dict[str, Any]]] = Modality.importers.new_child()
    exporters: MutableMapping[str, tuple[type[BaseExporter], dict[str, Any]]] = Modality.exporters.new_child()

    # Properties #
    @property
    def ieeg_metadata_path(self) -> Path:
        """The path to the ieeg metadata json file."""
        return self._path / f"{self.full_name}_ieeg.json"

    @property
    def ieeg_metadata(self) -> dict[str, Any]:
        """The ieeg metadata."""
        if self._ieeg_metadata is None:
            return self.default_ieeg_metadata.copy()
        else:
            return self._ieeg_metadata
    
    @property
    def coordinate_system_path(self) -> Path:
        """The path to the coordinate system json file."""
        return self._path / f"{self.full_name}_coordinatesystem.json"

    @property
    def coordinate_system(self) -> dict[str, Any]:
        """The coordinate system of the electrodes."""
        if self._coordinate_system is None:
            return self.default_coordinate_system.copy()
        else:
            return self._coordinate_system
    
    @property
    def electrodes_path(self) -> Path:
        """The path to the electrodes tsv file."""
        return self.path / f"{self.full_name}_electrodes.tsv"

    @property
    def channels_path(self) -> Path:
        """The path to the channels tsv file."""
        return self.path / f"{self.full_name}_channels.tsv"

    @property
    def events_path(self) -> Path:
        """The path to the stimulation events tsv file."""
        return self.path / f"{self.full_name}_events.tsv"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        path: Path | str | None = None,
        name: str | None = None,
        parent_path: Path | str | None = None,
        mode: str | None = None,
        create: bool = False,
        build: bool = True,
        load: bool = True,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.electrode_columns = self.electrode_columns.copy()
        self.channel_columns = self.channel_columns.copy()
        self.event_columns = self.event_columns.copy()

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                path=path,
                name=name,
                parent_path=parent_path,
                mode=mode,
                create=create,
                build=build,
                load=load,
                **kwargs,
            )

    # Instance Methods #
    def build(self) -> None:
        """Builds the IEEG structure and default files."""
        super().build()
        self.create_ieeg_metadata()

    # IEEG Metadata
    def create_ieeg_metadata(self) -> None:
        """Creates ieeg metadata file and saves the metadata."""
        if self._ieeg_metadata is None:
            self._ieeg_metadata = deepcopy(self.default_ieeg_metadata)
        with self.ieeg_metadata_path.open(self._mode) as file:
            json.dump(self._ieeg_metadata, file)

    def load_ieeg_data(self) -> dict:
        """Loads the ieeg metadata from the file.

        Returns:
            The ieeg metadata.
        """
        if self._ieeg_metadata is None:
            self._ieeg_metadata = {}
        else:
            self._ieeg_metadata.clear()

        with self.ieeg_metadata_path.open("r") as file:
            self._ieeg_metadata.update(json.load(file))

        return self._ieeg_metadata

    def save_ieeg_metadata(self) -> None:
        """Saves the ieeg metadata to the file."""
        with self.ieeg_metadata_path.open(self._mode) as file:
            json.dump(self.ieeg_metadata, file)
    
    # Coordinate System
    def create_coordinate_system(self) -> None:
        """Creates coordinate system file and saves the coordinate system."""
        if self._coordinate_system is None:
            self._coordinate_system = deepcopy(self.default_coordinate_system)
        with self.coordinate_system_path.open(self._mode) as file:
            json.dump(self._coordinate_system, file)

    def load_coordinate_system(self) -> dict:
        """Loads the coordinate system from the file.

        Returns:
            The electrode coordinate system.
        """
        if self._coordinate_system is None:
            self._coordinate_system = {}
        else:
            self._coordinate_system.clear()

        with self.coordinate_system_path.open("r") as file:
            self._coordinate_system.update(json.load(file))

        return self._coordinate_system

    def save_coordinate_system(self) -> None:
        """Saves the coordinate system to the file."""
        with self.coordinate_system_path.open(self._mode) as file:
            json.dump(self.coordinate_system, file)
    
    # Electrodes
    def create_electrodes(self) -> None:
        """Creates electrodes file and saves the electrodes."""
        if self.electrodes is None:
            self.electrodes = pd.DataFrame(columns=self.electrode_columns)

        self.electrodes.to_csv(self.electrodes_path, mode=self._mode, sep="\t")

    def load_electrodes(self) -> pd.DataFrame:
        """Loads the electrode information from the file.

        Returns:
            The electrode information.
        """
        self.electrodes = electrodes = pd.read_csv(self.electrodes_path, sep="\t")
        return electrodes

    def save_electrodes(self) -> None:
        """Saves the electrodes to the file."""
        self.electrodes.to_csv(self.electrodes_path, mode=self._mode, sep="\t")

    # Channels
    def create_channels(self) -> None:
        """Creates channels file and saves the channels."""
        if self.channels is None:
            self.channels = pd.DataFrame(columns=self.channel_columns)

        self.channels.to_csv(self.channels_path, mode=self._mode, sep="\t")

    def load_channels(self) -> pd.DataFrame:
        """Loads the channel information from the file.

        Returns:
            The channel information.
        """
        self.channels = channels = pd.read_csv(self.channels_path, sep="\t")
        return channels

    def save_channels(self) -> None:
        """Saves the channels to the file."""
        self.channels.to_csv(self.channels_path, mode=self._mode, sep="\t")

    # Stimulation Events
    def create_events(self) -> None:
        """Creates stimulation events file and saves the events."""
        if self.events is None:
            self.events = pd.DataFrame(columns=self.event_columns)

        self.events.to_csv(self.events_path, mode=self._mode, sep="\t")

    def load_events(self) -> pd.DataFrame:
        """Loads the stimulation event information from the file.

        Returns:
            The stimulation event information.
        """
        self.events = events = pd.read_csv(self.events_path, sep="\t")
        return events

    def save_events(self) -> None:
        """Saves the stimulation events to the file."""
        self.events.to_csv(self.events_path, mode=self._mode, sep="\t")
