from swh.graphql.backends import archive
from swh.model.model import Directory

from .base_node import BaseSWHNode


class BaseDirectoryNode(BaseSWHNode):
    def _get_directory_by_id(self, directory_id):
        # Return a Directory model object
        # entries is initialized as empty
        # Same pattern is used in snapshot
        return Directory(id=directory_id, entries=())

    def is_type_of(self):
        return "Directory"


class DirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested directly with its SWHID
        """
        directory_id = self.kwargs.get("SWHID").object_id
        # path = ""
        if archive.Archive().is_directory_available([directory_id]):
            return self._get_directory_by_id(directory_id)
        return None


class RevisionDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested from a revision
        self.obj is revision here
        self.obj.directorySWHID is the required dir SWHID
        (set from resolvers.revision.py:BaseRevisionNode)
        """
        directory_id = self.obj.directorySWHID.object_id
        return self._get_directory_by_id(directory_id)


class TargetDirectoryNode(BaseDirectoryNode):
    def _get_node_data(self):
        """
        When a directory is requested as a target
        self.obj can be a Release or a DirectoryEntry

        obj.targetHash is the requested directory id here
        """
        return self._get_directory_by_id(self.obj.targetHash)
