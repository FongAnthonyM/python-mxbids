""" basicstructure.py

"""
# Imports #
# Standard Libraries #
import pathlib

# Third-Party Packages #
from mxbids import Dataset, Subject, Session
from mxbids import Anatomy, CT, IEEG  # Import some Modalities


# Definitions #
# Classes #
# Specify some common session types
class FullSession(Session):
    # Set the default Modalities in this session
    # Dictionary of Name: (Modality Type, Modality Kwargs)
    default_modalities = {
        "anat": (Anatomy, {}),
        "ct": (CT, {}),
        "ieeg": (IEEG, {}),
    }


class ImagingSession(Session):
    # Set the default Modalities in this session
    default_modalities = {
        "anat": (Anatomy, {}),
        "ct": (CT, {}),
    }


class IEEGSession(Session):
    # Set the default Modalities in this session
    default_modalities = {
        "ieeg": (IEEG, {}),
    }


# Specify some common subject types
class TypicalSubject(Subject):
    # Set the default Sessions these Subjects will have
    default_sessions = {
        "DayOneImaging": (ImagingSession, {}),
        "FirstRecording": (IEEGSession, {}),
        "FollowUpFullSession": (FullSession, {}),
    }


# Execution #
if __name__ == "__main__":
    # Setup
    path = pathlib.Path.cwd().joinpath("BasicStructureExampleDataset")

    # Create Dataset
    print("\nCreating Dataset")
    dataset = Dataset(path, name="TestDataset", mode="w", create=True)

    # Create New Subjects
    print("\nCreating Subjects")
    sub_1 = dataset.create_subject("Subject0001")  # Empty Subject
    sub_2 = dataset.create_subject("Subject0002", TypicalSubject)  # A subject with a few initial sessions

    print("\nInitial Dataset Structure")
    dataset.print_children()

    # Create More Sessions
    print("\nCreating More Sessions")
    sub_1.create_session("RandomFullSession", FullSession)
    sub_2.create_session("SecondRecording", IEEGSession)

    print("\nUpdated Dataset Structure")
    dataset.print_children()

    # Close and Reopen Dataset
    del dataset
    dataset = Dataset(path, mode="r", load_subjects=True, load_sessions=True, load_modalities=True)

    print("\nReopened Dataset Structure")
    dataset.print_children()
