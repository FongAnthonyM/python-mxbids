#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package.
"""
# Package Header #
from ucsfbids.header import *

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
from ucsfbids.datasets import Dataset


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""

    class_ = None

    def test_instance_creation(self, *args, **kwargs):
        pass


# Base Object
class TestDataset(ClassTest):
    """Test the BaseObject class which a subclass is created to test with."""

    class_ = Dataset

    def create_dataset(self, tmp_dir):
        """Create the dataset."""
        dataset_path = tmp_dir / "subjects"
        dataset = self.class_(path=dataset_path, mode="w", create=True)
        return dataset

    def test_create(self, tmp_dir):
        dataset = self.create_dataset(tmp_dir)
        assert dataset.path.exists()

    def test_create_subject(self, tmp_dir):
        dataset = self.create_dataset(tmp_dir)
        subject = dataset.create_subject()
        assert subject.path.exists()

    def test_create_session(self, tmp_dir):
        dataset = self.create_dataset(tmp_dir)
        subject = dataset.create_subject()
        session = subject.create_session()
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
