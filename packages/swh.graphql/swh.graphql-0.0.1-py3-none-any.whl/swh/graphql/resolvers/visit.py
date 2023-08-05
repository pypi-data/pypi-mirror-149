from swh.graphql.backends import archive
from swh.graphql.utils import utils

from .base_connection import BaseConnection
from .base_node import BaseNode


class BaseVisitNode(BaseNode):
    @property
    def id(self):
        # FIXME, use a better id
        return utils.b64encode(f"{self.origin}-{str(self.visit)}")

    @property
    def visitId(self):  # To support the schema naming convention
        return self._node.visit


class OriginVisitNode(BaseVisitNode):
    """
    Get the visit directly with an origin URL and a visit ID
    """

    def _get_node_data(self):
        return archive.Archive().get_origin_visit(
            self.kwargs.get("originUrl"), int(self.kwargs.get("visitId"))
        )


class LatestVisitNode(BaseVisitNode):
    """
    Get the latest visit for an origin
    self.obj is the origin object here
    self.obj.url is the origin URL
    """

    def _get_node_data(self):
        return archive.Archive().get_origin_latest_visit(self.obj.url)


class OriginVisitConnection(BaseConnection):
    _node_class = BaseVisitNode

    def _get_paged_result(self):
        """
        Get the visits for the given origin
        parent obj (self.obj) is origin here
        """
        return archive.Archive().get_origin_visits(
            self.obj.url, after=self._get_after_arg(), first=self._get_first_arg()
        )
