"""Blob Host class
"""
from abc import ABCMeta, abstractmethod


class BLOBHost(object, metaclass=ABCMeta):
    def __init__(self, blob_host_uri, blob_host_user=None, blob_host_password=None):
        """Initializes blob host

        Args:
            blob_host_uri:
            blob_host_user:
            blob_host_password:
        """
        self.blob_host_uri = blob_host_uri
        self.blob_host_user = blob_host_user
        self.blob_host_password = blob_host_password

    @abstractmethod
    def save(self, blob, filename):
        """Saves a blob

        Args:
            blob: string or binaries
            filename:

        Returns: uri

        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def get(self, handle):
        """Returns a blob given its handle

        Args:
            handle:

        Returns: string or binaries

        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def list(self):
        """Lists blobs

        Returns: list of uris

        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def query(self, query):
        """Executes a query on list of blobs

        Args:
            query:

        Returns:

        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def delete(self, handle):
        """Deletes a blob pointed by the handle

        Args:
            handle:

        Returns:

        """
        raise NotImplementedError("This method is not implemented.")
