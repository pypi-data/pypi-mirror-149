from swh.graphql.backends import archive

from .base_node import BaseSWHNode


class BaseReleaseNode(BaseSWHNode):
    def _get_release_by_id(self, release_id):
        return (archive.Archive().get_releases([release_id]) or None)[0]

    @property
    def targetHash(self):  # To support the schema naming convention
        return self._node.target

    @property
    def targetType(self):  # To support the schema naming convention
        return self._node.target_type.value

    def is_type_of(self):
        """
        is_type_of is required only when resolving
        a UNION type
        This is for ariadne to return the right type
        """
        return "Release"


class ReleaseNode(BaseReleaseNode):
    """
    When the release is requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_release_by_id(self.kwargs.get("SWHID").object_id)


class TargetReleaseNode(BaseReleaseNode):
    """
    When a release is requested as a target

    self.obj could be a snapshotbranch or a release
    self.obj.targetHash is the requested release id here
    """

    def _get_node_data(self):
        return self._get_release_by_id(self.obj.targetHash)
