from collections import namedtuple

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SnapshotBranchNode(BaseNode):
    """
    target field for this Node is a UNION in the schema
    It is resolved in resolvers.resolvers.py
    """

    def _get_node_from_data(self, node_data):
        """
        node_data is not a dict in this case
        overriding to support this special data structure
        """

        # STORAGE-TODO; return an object in the normal format
        branch_name, branch_obj = node_data
        node = {
            "name": branch_name,
            "type": branch_obj.target_type.value,
            "target": branch_obj.target,
        }
        return namedtuple("NodeObj", node.keys())(*node.values())

    @property
    def targetHash(self):  # To support the schema naming convention
        return self._node.target


class SnapshotBranchConnection(BaseConnection):
    _node_class = SnapshotBranchNode

    def _get_paged_result(self):
        """
        When branches requested from a snapshot
        self.obj.SWHID is the snapshot SWHID here
        (as returned from resolvers/snapshot.py)
        """

        result = archive.Archive().get_snapshot_branches(
            self.obj.SWHID.object_id,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            target_types=self.kwargs.get("types"),
            name_include=self.kwargs.get("nameInclude"),
        )
        # FIXME Cursor must be a hex to be consistent with
        # the base class, hack to make that work
        end_cusrsor = (
            result["next_branch"].hex() if result["next_branch"] is not None else None
        )
        # FIXME, this pagination is not consistent with other connections
        # FIX in swh-storage to return PagedResult
        # STORAGE-TODO
        return PagedResult(
            results=result["branches"].items(), next_page_token=end_cusrsor
        )

    def _get_after_arg(self):
        """
        Snapshot branch is using a different cursor; logic to handle that
        """
        # FIXME Cursor must be a hex to be consistent with
        # the base class, hack to make that work
        after = utils.get_decoded_cursor(self.kwargs.get("after", ""))
        return bytes.fromhex(after)
