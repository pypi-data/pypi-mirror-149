from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.model.swhids import CoreSWHID, ObjectType

from .base_connection import BaseConnection
from .base_node import BaseSWHNode


class BaseRevisionNode(BaseSWHNode):
    def _get_revision_by_id(self, revision_id):
        return (archive.Archive().get_revisions([revision_id]) or None)[0]

    @property
    def parentSWHIDs(self):  # To support the schema naming convention
        return [
            CoreSWHID(object_type=ObjectType.REVISION, object_id=parent_id)
            for parent_id in self._node.parents
        ]

    @property
    def directorySWHID(self):  # To support the schema naming convention
        """ """
        return CoreSWHID(
            object_type=ObjectType.DIRECTORY, object_id=self._node.directory
        )

    @property
    def type(self):
        return self._node.type.value

    def is_type_of(self):
        """
        is_type_of is required only when resolving
        a UNION type
        This is for ariadne to return the right type
        """
        return "Revision"


class RevisionNode(BaseRevisionNode):
    """
    When the revision is requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_revision_by_id(self.kwargs.get("SWHID").object_id)


class TargetRevisionNode(BaseRevisionNode):
    """
    When a revision is requested as a target

    self.obj could be a snapshotbranch or a release
    self.obj.targetHash is the requested revision id here
    """

    def _get_node_data(self):
        return self._get_revision_by_id(self.obj.targetHash)


class ParentRevisionConnection(BaseConnection):
    """
    When parent revisions is requested from a
    revision
    self.obj is the current(child) revision
    self.obj.parentSWHIDs is the list of
    parent SWHIDs
    """

    _node_class = BaseRevisionNode

    def _get_paged_result(self):
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        parents = archive.Archive().get_revisions(
            [x.object_id for x in self.obj.parentSWHIDs]
        )
        return utils.paginated(parents, self._get_first_arg(), self._get_after_arg())


class LogRevisionConnection(BaseConnection):
    """
    When revisionslog is requested from a
    revision
    self.obj is the current revision id
    """

    _node_class = BaseRevisionNode

    def _get_paged_result(self):
        # STORAGE-TODO (date in revisionlog is a dict)
        log = archive.Archive().get_revision_log([self.obj.SWHID.object_id])
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        return utils.paginated(log, self._get_first_arg(), self._get_after_arg())
