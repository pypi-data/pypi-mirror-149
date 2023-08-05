"""DSpace Blob Host class
"""
from blob_utils.blob_host import BLOBHost


class DSpaceBLOBHost(BLOBHost):
    def __init__(self, blob_host_uri, blob_host_user, blob_host_password):
        """Initializes DSpace blob host

        Args:
            blob_host_uri:
            blob_host_user:
            blob_host_password:
        """
        BLOBHost.__init__(self, blob_host_uri, blob_host_user, blob_host_password)

    def get(self, handle):
        BLOBHost.get(self, handle)

    def list(self):
        BLOBHost.list(self)

    def save(self, blob, filename=None):
        BLOBHost.save(self, blob, filename)

    def delete(self, handle):
        BLOBHost.delete(self, handle)

    def query(self, query):
        BLOBHost.query(self, query)
