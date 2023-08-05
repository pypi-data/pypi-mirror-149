"""Blob host factory
"""

from blob_utils.commons.exceptions import BLOBError
from blob_utils.dspace_blob_host import DSpaceBLOBHost
from blob_utils.gridfs_blob_host import GridFSBLOBHost


class BLOBHostFactory(object):
    BLOB_HOSTS = ["DSPACE", "GRIDFS"]

    def __init__(
        self,
        blob_host=None,
        blob_host_uri=None,
        blob_host_user=None,
        blob_host_password=None,
    ):
        """Initialize Blob host factory.

        Args:
            blob_host:
            blob_host_uri:
            blob_host_user:
            blob_host_password:
        """
        self.blob_host = str(blob_host).upper() if blob_host is not None else None
        self.blob_host_uri = str(blob_host_uri) if blob_host_uri is not None else None
        self.blob_host_user = (
            str(blob_host_user) if blob_host_user is not None else None
        )
        self.blob_host_password = (
            str(blob_host_password) if blob_host_password is not None else None
        )

    def create_blob_host(self):
        """Returns a blob host

        Returns:

        """
        if self.blob_host is not None and self.blob_host in self.BLOB_HOSTS:
            if self.blob_host == self.BLOB_HOSTS[0]:
                return self._create_dspace_host()
            elif self.blob_host == self.BLOB_HOSTS[1]:
                return self._create_gridfs_host()
        else:
            raise BLOBError("BLOB_HOST should take a value in " + str(self.BLOB_HOSTS))

    def _create_dspace_host(self):
        """Returns a DSpace host

        Returns:

        """
        if (
            self.blob_host_uri is not None
            and self.blob_host_user is not None
            and self.blob_host_password is not None
        ):
            return DSpaceBLOBHost(
                self.blob_host_uri, self.blob_host_user, self.blob_host_password
            )
        else:
            raise BLOBError(
                "BLOB_HOST_URI, BLOB_HOST_USER and BLOB_HOST_PASSWORD should be set."
            )

    def _create_gridfs_host(self):
        """Returns a GridFS host

        Returns:

        """
        if self.blob_host_uri is not None:
            return GridFSBLOBHost(self.blob_host_uri)
        else:
            raise BLOBError("BLOB_HOST_URI should be set.")
