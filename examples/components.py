""" components.py

"""
# Imports #
# Standard Libraries #
import pathlib
import random

# Third-Party Packages #
from baseobjects.composition import BaseComponent
import pandas as pd

from mxbids import Dataset, Subject, Session
from mxbids import IEEG  # The IEEG Modality


# Definitions #
# Classes #
# Create a new component to extend IEEG Modality
class NewIEEGComponent(BaseComponent):

    def create_random_electrodes(self):
        """Generates random electrode information for the IEEG object.
    
        Returns:
            A pandas dataframe containing mock data for electrode locations and labels.
        """
        xs = random.sample(range(-100, 100), 10)
        ys = random.sample(range(-100, 100), 10)
        zs = random.sample(range(-100, 100), 10)
        names = tuple(f"electrode_{n}" for n in range(1, 11))
        groups = random.sample(("grid", "stereo"), 10)

        montage = pd.DataFrame(columns=self.composite.electrode_columns)
        montage.loc[:, "x"] = xs
        montage.loc[:, "y"] = ys
        montage.loc[:, "z"] = zs
        montage.loc[:, "name"] = names
        montage.loc[:, "group"] = groups
        montage.loc[:, "size"] = "n/a"
        montage.loc[:, "material"] = "n/a"
        montage.loc[:, "manufacturer"] = "n/a"
        montage.loc[montage["x"] > 0, "hemisphere"] = "r"
        montage.loc[montage["x"] <= 0, "hemisphere"] = "l"
        montage.loc[:, "type"] = "n/a"
        montage.loc[:, "impedance"] = "n/a"
        montage.name = montage.name.fillna("NaN")

        return montage

    def number_of_grid_electrodes(self):
        return len(self.composite.electrodes[self.composite.electrodes["group"] == "grid"])


# Register it
IEEG.component_types_register.register_class(NewIEEGComponent)


# Create a new Modality with the Component
class IEEGWithNewComponent(IEEG):
    # Set the default components in this IEEG Modality
    # Dictionary of Name: (Component Type, Component Kwargs)
    default_component_types = {
        "random_electrode_generator": (NewIEEGComponent, {}),
    }



# Create a new component to extend a Session
class TextFileComponent(BaseComponent):

    # Attributes #
    file_name: str = "text_file.txt"
    text: str = ""

    # Magic Methods #
    def __init__(self, name: str | None = None, text: str | None = None, *args, **kwargs):
        # Override Attributes
        if name is not None:
            self.file_name = name

        if text is not None:
            self.text = text

        # Call Parent Init
        super().__init__(*args, **kwargs)

    # Instance Methods #
    def create_text_file(self):
        file_path = self.composite.path / self.file_name
        if not file_path.exists():
            with file_path.open("w") as f:
                f.write(self.text)

    def read_text_file(self):
        file_path = self.composite.path / self.file_name
        if file_path.exists():
            with file_path.open("r") as f:
                text = f.read()
            print(f"Text file contents:\n{text}")
        else:
            print("Text file not found.")


# Register it
Session.component_types_register.register_class(TextFileComponent)


# Create a new Session with the Component
class SessionWithNewComponent(Session):
    # Set the default components in this IEEG Modality
    # Dictionary of Name: (Component Type, Component Kwargs)
    default_component_types = {
        "hello_text_file": (TextFileComponent, {"name": "hello_file.text", "text": "Hello World!"}),
        "second_text_file": (TextFileComponent, {"name": "second_file.text", "text": "Second Text!"}),
    }
    default_modalities = {
        "ieeg": (IEEGWithNewComponent, {}),
    }

# Note Components for Subjects and Dataset can be made in the same way! (not including for brevity)


# Execution #
if __name__ == "__main__":
    # Setup
    path = pathlib.Path.cwd().joinpath("ComponentsExampleDataset")

    # Create Dataset
    print("\nCreating Dataset")
    dataset = Dataset(path, name="TestDataset", mode="w", create=True)

    # Create New Subjects
    print("\nCreating Subjects")
    sub_1 = dataset.create_subject("Subject0001")  # Empty Subject

    print("\nInitial Dataset Structure")
    dataset.print_children()


    # Create More Sessions
    print("\nUsing Components")
    # Create Session
    session_1 = sub_1.create_session("SessionFromNewType", session=SessionWithNewComponent)

    # Using Default Components
    session_1.components["hello_text_file"].create_text_file()
    session_1.components["hello_text_file"].read_text_file()

    second_component = session_1.components["second_text_file"]
    second_component.text = "We have crazy flexibility"
    second_component.create_text_file()
    second_component.read_text_file()

    # Adding Components Later
    session_2 = sub_1.create_session("SessionWasDefault")
    new_component = session_2.create_component("new_file", component=TextFileComponent, text="New Text")
    new_component.file_name = "new_file.txt"
    new_component.create_text_file()
    new_component.read_text_file()

    print("\nUpdated Dataset Structure")
    dataset.print_children()

    # Close Dataset
    del dataset, sub_1, session_1, session_2, second_component, new_component


    # Reopen Dataset #
    dataset = Dataset(path, mode="r", load_subjects=True, load_sessions=True, load_modalities=True)

    print("\nReopened Dataset Structure")
    dataset.print_children()

    # Loading Components
    print("\nLoading Components")
    subject = dataset.subjects["Subject0001"]

    session_1 = subject.sessions["SessionFromNewType"]
    session_1.components["hello_text_file"].read_text_file()
    session_1.components["second_text_file"].read_text_file()
    #
    # session_2 = subject.sessions["SessionWasDefault"]
    # session_2.components["new_text_file"].read_text_file()
