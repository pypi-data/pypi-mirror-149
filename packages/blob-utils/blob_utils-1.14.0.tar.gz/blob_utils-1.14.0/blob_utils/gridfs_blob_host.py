""" GridFS Blob Host
"""
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient

from blob_utils.blob_host import BLOBHost
from blob_utils.commons.exceptions import BLOBError

CONNECTION_TIMEOUT = 100


class GridFSBLOBHost(BLOBHost):
    def __init__(self, blob_host_uri):
        """Initialize GridFS blob host.

        Args:
            blob_host_uri: MongoDB uri (mongodb://username:password@host:port/database)
        """
        BLOBHost.__init__(self, blob_host_uri)

        try:
            # connect to mongo instance
            self.client = MongoClient(
                self.blob_host_uri, serverSelectionTimeoutMS=CONNECTION_TIMEOUT
            )
            # check connection
            self.client.server_info()
            # get database name from uri
            database_name = blob_host_uri.split("/")[-1]
            # connect to database
            self.database = self.client[database_name]
            # connect to gridfs
            self.fs = gridfs.GridFS(self.database)
        except Exception as e:
            raise BLOBError(
                "Unable to create the connection to the GridFS collection: %s" % str(e)
            )

    def get(self, handle):
        """Return a blob with the given handle.

        Args:
            handle(str): ObjectId of the Blob object to retrieve.

        Returns:
            bytes: the content of the file stored with the given Blob id.

        Raises:
            BlobError: if the object does not exists or an unexpected error occurs.
        """
        try:
            if not self.fs.exists(ObjectId(handle)):
                raise BLOBError("No file found with the given ID.")

            with self.fs.get(ObjectId(handle)) as blob:
                return blob.read()
        except Exception as exc:
            raise BLOBError(
                f"An unexpected error occurred while retrieving the file: {str(exc)}"
            )

    def list(self):
        """Return list of blob ids.

        Returns:
        """
        return [str(blob._id) for blob in self.fs.find()]

    def save(self, blob, filename=None, metadata=None):
        """Save a blob.

        Args:
            blob:
            filename:
            metadata:

        Returns:

        """
        try:
            if metadata is None:
                metadata = dict()

            blob_id = self.fs.put(blob, filename=filename, metadata=metadata)
        except Exception as exc:
            raise BLOBError(f"An error occurred while saving the file: {str(exc)}")
        return blob_id

    def delete(self, handle):
        """Delete a blob

        Args:
            handle: blob id

        Returns:

        """
        try:
            if self.fs.exists(ObjectId(handle)):
                self.fs.delete(ObjectId(handle))
        except Exception as exc:
            raise BLOBError(f"An error occurred while deleting the file: {str(exc)}")

    def query(self, query):
        """Query the blob collection. Not yet implemented.

        Args:
            query:

        Returns:

        """
        BLOBHost.query(self, query)
