from swh.graphql.backends import archive

from .base_connection import BaseConnection
from .base_node import BaseSWHNode


class OriginNode(BaseSWHNode):
    def _get_node_data(self):
        return archive.Archive().get_origin(self.kwargs.get("url"))


class OriginConnection(BaseConnection):
    _node_class = OriginNode

    def _get_paged_result(self):
        return archive.Archive().get_origins(
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            url_pattern=self.kwargs.get("urlPattern"),
        )
