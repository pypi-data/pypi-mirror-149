from swh.graphql.backends import archive

from .base_node import BaseSWHNode


class BaseContentNode(BaseSWHNode):
    """ """

    def _get_content_by_id(self, content_id):
        content = archive.Archive().get_content(content_id)
        return content[0] if content else None

    @property
    def checksum(self):
        # FIXME, return a Node object
        return self._node.hashes()

    @property
    def id(self):
        return self._node.sha1_git

    def is_type_of(self):
        return "Content"


class ContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested directly
        with its SWHID
        """
        return self._get_content_by_id(self.kwargs.get("SWHID").object_id)


class TargetContentNode(BaseContentNode):
    def _get_node_data(self):
        """
        When a content is requested from a
        directory entry or from a release target

        content id is obj.targetHash here
        """
        content_id = self.obj.targetHash
        return self._get_content_by_id(content_id)
