"""Tests for GridFS Host
"""
from os.path import join, dirname, abspath
from unittest import TestCase

from blob_utils.blob_host_factory import BLOBHostFactory
from blob_utils.commons.exceptions import BLOBError
from tests.test_settings import MONGODB_URI

RESOURCES_PATH = join(dirname(abspath(__file__)), "data")


class TestGridFSHost(TestCase):
    blob_host = None

    @classmethod
    def setUpClass(cls):
        blob_host_factory = BLOBHostFactory("GridFS", MONGODB_URI)
        cls.blob_host = blob_host_factory.create_blob_host()

        if len(list(cls.blob_host.fs.find())) != 0:
            raise BLOBError("Unable to perform the tests if the database is not empty.")

    def test_save(self):
        with open(join(RESOURCES_PATH, "test.xml"), "rb") as test_file:
            blob_id = TestGridFSHost.blob_host.save(test_file)

        self.blob_host.fs.delete(blob_id)
        self.assertTrue(blob_id is not None)

    def test_get_returns_same_content(self):
        with open(join(RESOURCES_PATH, "test.xml"), "rb") as test_file:
            blob_id = TestGridFSHost.blob_host.save(test_file)

        retrieved_blob = TestGridFSHost.blob_host.get(blob_id)

        self.blob_host.fs.delete(blob_id)
        self.assertTrue(
            retrieved_blob == open(join(RESOURCES_PATH, "test.xml"), "rb").read()
        )

    def test_get_returns_same_image(self):
        with open(join(RESOURCES_PATH, "collapse.png"), "rb") as test_file:
            blob_id = TestGridFSHost.blob_host.save(test_file)

        retrieved_blob = TestGridFSHost.blob_host.get(blob_id)

        self.blob_host.fs.delete(blob_id)
        self.assertTrue(
            retrieved_blob == open(join(RESOURCES_PATH, "collapse.png"), "rb").read()
        )

    def test_list_0_element(self):
        self.assertTrue(TestGridFSHost.blob_host.list() == [])

    def test_list_1_element(self):
        with open(join(RESOURCES_PATH, "test.xml"), "rb") as test_file:
            blob_id = TestGridFSHost.blob_host.save(test_file)

        self.assertTrue(TestGridFSHost.blob_host.list() == [str(blob_id)])
        self.blob_host.fs.delete(blob_id)

    def test_delete(self):
        with open(join(RESOURCES_PATH, "test.xml"), "rb") as test_file:
            blob_id = TestGridFSHost.blob_host.save(test_file)

        self.blob_host.delete(blob_id)
        self.assertTrue(list(TestGridFSHost.blob_host.fs.find()) == [])
