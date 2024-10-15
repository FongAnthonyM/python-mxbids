#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package.
"""
# Package Header #
from mxbids.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import abc
import pathlib

# Third-Party Packages #
import pytest

# Local Packages #
from mxbids import Dataset
from mxbids.cdfsbids import CDFSSession


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class TestDataset:
    """Test the BaseObject class which a subclass is created to test with."""

    def create_dataset(self, tmp_dir):
        """Create the dataset."""
        dataset_path = tmp_dir / "subjects"
        dataset = Dataset(path=dataset_path, mode="w", create=True)
        return dataset

    def test_create_session(self, tmp_dir):
        dataset = self.create_dataset(tmp_dir)
        subject = dataset.create_subject()
        session = subject.create_session(session=CDFSSession)
        assert session.path.exists()

    def test_create_modality(self, tmp_dir):
        dataset = self.create_dataset(tmp_dir)
        subject = dataset.create_subject()
        session = subject.create_session()
        modality = session.create_modality("test_modality")
        assert modality.path.exists()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
