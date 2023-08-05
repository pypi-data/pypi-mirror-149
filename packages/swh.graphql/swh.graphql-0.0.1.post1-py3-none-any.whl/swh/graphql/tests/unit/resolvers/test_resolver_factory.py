import pytest

from swh.graphql.resolvers import resolver_factory


class TestFactory:
    @pytest.mark.parametrize(
        "input_type, expexted",
        [
            ("origin", "OriginNode"),
            ("visit", "OriginVisitNode"),
            ("latest-visit", "LatestVisitNode"),
            ("latest-status", "LatestVisitStatusNode"),
            ("visit-snapshot", "VisitSnapshotNode"),
            ("snapshot", "SnapshotNode"),
            ("branch-revision", "TargetRevisionNode"),
            ("branch-release", "TargetReleaseNode"),
            ("revision", "RevisionNode"),
            ("revision-directory", "RevisionDirectoryNode"),
            ("release", "ReleaseNode"),
            ("release-revision", "TargetRevisionNode"),
            ("release-release", "TargetReleaseNode"),
            ("release-directory", "TargetDirectoryNode"),
            ("release-content", "TargetContentNode"),
            ("directory", "DirectoryNode"),
            ("content", "ContentNode"),
            ("dir-entry-dir", "TargetDirectoryNode"),
            ("dir-entry-file", "TargetContentNode"),
        ],
    )
    def test_get_node_resolver(self, input_type, expexted):
        response = resolver_factory.get_node_resolver(input_type)
        assert response.__name__ == expexted

    def test_get_node_resolver_invalid_type(self):
        with pytest.raises(AttributeError):
            resolver_factory.get_node_resolver("invalid")

    @pytest.mark.parametrize(
        "input_type, expexted",
        [
            ("origins", "OriginConnection"),
            ("origin-visits", "OriginVisitConnection"),
            ("origin-snapshots", "OriginSnapshotConnection"),
            ("visit-status", "VisitStatusConnection"),
            ("snapshot-branches", "SnapshotBranchConnection"),
            ("revision-parents", "ParentRevisionConnection"),
            ("revision-log", "LogRevisionConnection"),
            ("directory-entries", "DirectoryEntryConnection"),
        ],
    )
    def test_get_connection_resolver(self, input_type, expexted):
        response = resolver_factory.get_connection_resolver(input_type)
        assert response.__name__ == expexted

    def test_get_connection_resolver_invalid_type(self):
        with pytest.raises(AttributeError):
            resolver_factory.get_connection_resolver("invalid")
