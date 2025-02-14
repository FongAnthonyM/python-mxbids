""" basics.py
This tutorial demonstrates the complete workflow for creating, managing, and loading a dataset 
using the MXBIDS library. It includes steps for setting up a dataset, creating subjects, sessions, 
and modalities, and showcases how to load and manage these objects either directly or hierarchically.
"""
# Imports #
# Standard Libraries
import pathlib

# Third-Party Packages
from mxbids import Dataset, Subject, Session, Modality
from mxbids.modalities import Anatomy


# Execution #
# Setup
path = pathlib.Path.cwd().joinpath("BasicExampleDataset")


# Creation #
# Create Dataset
print("\nCreating Dataset")
# Note: To create files on the system, both mode and create must be set to create them.
# Dataset
dataset = Dataset(path, name="TestDataset", mode="w", create=True)  # Both mode and create must be set to create the dataset

# Print Contents
print(f"Dataset created at {dataset.path}: {dataset.path.is_dir()}")


# Create Subjects
print("\nCreating Subjects")
# Note: The mode for creating new files inherits from the owning object, in this case is dataset.
# Subject with default settings
subject_1 = dataset.create_subject()  # Automatically generates subject name

# Subject with a few changed settings
subject_2 = dataset.create_subject(name="Subject0002", mode="w", create=True)  # Can override mode and create

# Subject of a specific type
class SubjectExample(Subject):
    """Example of a custom Subject class."""

subject_3 = dataset.create_subject(name="Subject0003", subject=SubjectExample, mode="w", create=True)

# Print Contents
print(f"Subject Created: Name={subject_1.name}, Path={subject_1.path}")
print(f"Subject Created: Name={subject_2.name}, Path={subject_2.path}")
print(f"Subject Created: Name={subject_3.name}, Path={subject_3.path}, type={subject_3.__class__.__name__}")


# Create Session
print("Creating Sessions")
# Note: The mode for creating new files inherits from the owning object, in this case is subject.
# Session with default settings
session_1 = subject_1.create_session(name="Experiment01")

# Subject with a few changed settings
session_2 = subject_2.create_session(name="SubjectImagingOnly", mode="w", create=True)  # Can override mode and create

# Session of a specific type
class SessionExample(Session):
    """Example of a custom Session class."""

session_3 = subject_1.create_session(name="SubjectImagingOnly", session=SessionExample)

# Print Contents
print(f"Session Created: Name={session_1.name}, Path={session_1.path}")
print(f"Session Created: Name={session_3.name}, Path={session_3.path}, type={session_3.__class__.__name__}")


# Create Modality
print("Creating Modality")
# Note: The mode for creating new files inherits from the owning object, in this case is session.
# Modality with default settings
modality_1 = session_2.create_modality(name="anat")

# Modality a few changed settings
modality_2 = session_3.create_modality(name="anat", mode="w", create=True)  # Can override mode and create

# Modality of a specific type
class ModalityExample(Modality):
    """Example of a custom Modality class."""

modality_3 = session_1.create_modality(name="ieeg", modality=ModalityExample, mode="w", create=True)

# Modality of a specific type (Anatomy is a pre-made modality type which can be imported)
modality_4 = session_1.create_modality(name="anat", modality=Anatomy)

# Print Contents
print(f"Modality Created: Name={modality_1.name}, Path={modality_1.path}")
print(f"Modality Created: Name={modality_3.name}, Path={modality_3.path}, type={modality_3.__class__.__name__}")


# Delete objects to test loading (objects will automatically close upon deletion)
del dataset, subject_1, subject_2, subject_3
del session_1, session_2, session_3, modality_1, modality_2, modality_3, modality_4


# Loading
# Load Dataset
print("\nLoad Dataset")
# Note: Mode is read by default
# Load Dataset Without Subjects Loaded
# A Dataset is loaded but none of the subjects are loaded to reduce load overhead.
dataset_1 = Dataset(path)  # Mode is read by default

# Load Dataset and All Subjects
dataset_2 = Dataset(path, load_subjects=True)

# Load Dataset and Specific Subjects
# Can provide an Iterable of Subject names to load to get the best of both worlds
dataset_3 = Dataset(path, load_subjects=["S0000", "Subject0003"])

# Print Content
print(f"Dataset Loaded: Name={dataset_1.name}, Path={dataset_1.path}, Subjects={dataset_1.subjects.keys()}")
print(f"Dataset Loaded: Name={dataset_2.name}, Path={dataset_2.path}, Subjects={dataset_2.subjects.keys()}")
print(f"Dataset Loaded: Name={dataset_3.name}, Path={dataset_3.path}, Subjects={dataset_3.subjects.keys()}")


# Load Subjects
print(f"\nLoad Subjects")
# Load using Dataset
# More directly control loading from a data using load_subjects
print(f"Subjects: {dataset_1.subjects.keys()}")

dataset_1.load_subjects()  # Loads all subjects recursively
dataset_1.load_subjects(load=False)  # Loads Subjects but not their contents recursively
dataset_1.load_subjects(names=["SOOOO", "Subject0003"])  # Loads a subset of Subjects
dataset_1.load_subjects(clear=False)  # Determines if the subjects register will be cleared before loading
dataset_1.load_subjects()

print(f"Subjects: {dataset_1.subjects.keys()}")

# Get Subject from Dataset
subject = dataset_1.subjects["S0000"]
print(f"Subject Loaded: Name={subject.name}, Path={subject.path}, Exists={subject.path.exists()}")


# Load Directly
# A dataset is not needed to load a Subject
# (Note: This subject will not be in dataset register if loaded directly)
# Load with Full Path
subject_1 = Subject(path=path / "sub-S0000")

# Load with Parent and Subject Name
subject_2 = Subject(name= "Subject0002", parent_path=path)

# Print Contents
print(f"Subject Loaded: Name={subject_1.name}, Path={subject_1.path}, Exists={subject_1.path.exists()}")
print(f"Subject Loaded: Name={subject_2.name}, Path={subject_2.path}, Exists={subject_2.path.exists()}")


# Load Sessions
print(f"\nLoad Sessions")
# Load using Subjects
# More directly control loading of sessions using load_sessions
print(f"Sessions for Subject S0000: {subject.sessions.keys()}")

subject.load_sessions()  # Loads all sessions recursively
subject.load_sessions(load=False)  # Loads Sessions but not their contents recursively
subject.load_sessions(names=["Experiment01", "SubjectImagingOnly"])  # Loads a subset of Sessions
subject.load_sessions(clear=False)  # Determines if the sessions register will be cleared before loading
subject.load_sessions()

print(f"Sessions for Subject S0000: {subject.sessions.keys()}")

# Get Session
session = subject.sessions["Experiment01"]
print(f"Session Loaded: Name={session.name}, Path={session.path}, Exists={session.path.exists()}")


# Load Directly
# A subject is not needed to load a Session
# (Note: This session will not be in subject register if loaded directly)
# Load with Full Path
session_1 = Session(path=path / "sub-S0000" / "ses-Experiment01")

# Load with Parent and Session Name
session_2 = Session(name="SubjectImagingOnly", parent_path=path / "sub-Subject0002")

# Print Contents
print(f"Session Loaded: Name={session_1.name}, Path={session_1.path}, Exists={session_1.path.exists()}")
print(f"Session Loaded: Name={session_2.name}, Path={session_2.path}, Exists={session_2.path.exists()}")


# Load Modalities
print(f"\nLoad Modalities")
# Load using Sessions
# More directly control loading of modalities using load_modalities
# Modalities are loaded automatically so we will clear them for the example
session_1.modalities.clear()
print(f"Modalities for Session Experiment01: {session_1.modalities.keys()}")

session_1.load_modalities()  # Loads all modalities recursively
session_1.load_modalities(load=False)  # Loads Modalities but not their contents recursively
session_1.load_modalities(names=["anat", "ieeg"])  # Loads a subset of Modalities
session_1.load_modalities(clear=False)  # Determines if the modalities register will be cleared before loading
session_1.load_modalities()

print(f"Modalities for Session Experiment01: {session_1.modalities.keys()}")

# Get Modality
modality = session_1.modalities["anat"]
print(f"Modality Loaded: Name={modality.name}, Path={modality.path}, Exists={modality.path.exists()}")


# Load Directly
# A session is not needed to load a Modality
# (Note: This modality will not be in session register if loaded directly)
# Load with Full Path
modality_1 = Modality(path=path / "sub-S0000" / "ses-Experiment01" / "anat")

# Load with Parent and Modality Name
modality_2 = Modality(name="ieeg", parent_path=path / "sub-Subject0002" / "ses-SubjectImagingOnly")

# Print Contents
print(f"Modality Loaded: Name={modality_1.name}, Path={modality_1.path}, Exists={modality_1.path.exists()}")
print(f"Modality Loaded: Name={modality_2.name}, Path={modality_2.path}, Exists={modality_2.path.exists()}")

# Delete objects
del dataset_1, dataset_2
del subject, subject_1, subject_2, session, session_1, session_2, modality, modality_1, modality_2


# Fancy loading
print("\nFancy Loading")

# Full Loading
# When the loading is set to True, all objects at their respective levels are loaded.
print("\nFull Loading")
dataset = Dataset(path, load_subjects=True, load_sessions=True, load_modalities=True)
dataset.print_children()
del dataset

# Specific Loading
# When specific loads are given, only specific objects are loaded, acting as content filters.
# Saves compute and memory when looking for specific content across the hierarchy.
print("\nSpecific Loading")
dataset = Dataset(path, load_subjects=["S0000", "Subject0002"], load_sessions=["SubjectImagingOnly"], load_modalities=["anat"])
dataset.print_children()

