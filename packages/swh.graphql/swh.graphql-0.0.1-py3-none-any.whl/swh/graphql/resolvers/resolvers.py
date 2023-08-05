"""
High level resolvers
Any schema attribute can be resolved by any of the following ways
and in the following priority order
- In this module using an annotation  (eg: @visitstatus.field("snapshot"))
- As a property in the Node object (eg: resolvers.visit.OriginVisitNode.id)
- As an attribute/item in the object/dict returned by the backend (eg: Origin.url)
"""
from ariadne import ObjectType, UnionType
from graphql.type import GraphQLResolveInfo

from swh.graphql import resolvers as rs

from .resolver_factory import get_connection_resolver, get_node_resolver

query: ObjectType = ObjectType("Query")
origin: ObjectType = ObjectType("Origin")
visit: ObjectType = ObjectType("Visit")
visit_status: ObjectType = ObjectType("VisitStatus")
snapshot: ObjectType = ObjectType("Snapshot")
snapshot_branch: ObjectType = ObjectType("Branch")
revision: ObjectType = ObjectType("Revision")
release: ObjectType = ObjectType("Release")
directory: ObjectType = ObjectType("Directory")
directory_entry: ObjectType = ObjectType("DirectoryEntry")

branch_target: UnionType = UnionType("BranchTarget")
release_target: UnionType = UnionType("ReleaseTarget")
directory_entry_target: UnionType = UnionType("DirectoryEntryTarget")

# Node resolvers
# A node resolver should return an instance of BaseNode


@query.field("origin")
def origin_resolver(obj: None, info: GraphQLResolveInfo, **kw) -> rs.origin.OriginNode:
    """ """
    resolver = get_node_resolver("origin")
    return resolver(obj, info, **kw)()


@origin.field("latestVisit")
def latest_visit_resolver(
    obj: rs.origin.OriginNode, info: GraphQLResolveInfo, **kw
) -> rs.visit.LatestVisitNode:
    """ """
    resolver = get_node_resolver("latest-visit")
    return resolver(obj, info, **kw)()


@query.field("visit")
def visit_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.visit.OriginVisitNode:
    """ """
    resolver = get_node_resolver("visit")
    return resolver(obj, info, **kw)()


@visit.field("latestStatus")
def latest_visit_status_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.visit_status.LatestVisitStatusNode:
    """ """
    resolver = get_node_resolver("latest-status")
    return resolver(obj, info, **kw)()


@query.field("snapshot")
def snapshot_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.snapshot.SnapshotNode:
    """ """
    resolver = get_node_resolver("snapshot")
    return resolver(obj, info, **kw)()


@visit_status.field("snapshot")
def visit_snapshot_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.snapshot.VisitSnapshotNode:
    resolver = get_node_resolver("visit-snapshot")
    return resolver(obj, info, **kw)()


@snapshot_branch.field("target")
def snapshot_branch_target_resolver(
    obj: rs.snapshot_branch.SnapshotBranchNode, info: GraphQLResolveInfo, **kw
):
    """
    Snapshot branch target can be a revision or a release
    """
    resolver_type = f"branch-{obj.type}"
    resolver = get_node_resolver(resolver_type)
    return resolver(obj, info, **kw)()


@query.field("revision")
def revision_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.revision.RevisionNode:
    resolver = get_node_resolver("revision")
    return resolver(obj, info, **kw)()


@revision.field("directory")
def revision_directory_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.directory.RevisionDirectoryNode:
    resolver = get_node_resolver("revision-directory")
    return resolver(obj, info, **kw)()


@query.field("release")
def release_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.release.ReleaseNode:
    resolver = get_node_resolver("release")
    return resolver(obj, info, **kw)()


@release.field("target")
def release_target_resolver(obj, info: GraphQLResolveInfo, **kw):
    """
    release target can be a release, revision,
    directory or content
    obj is release here, target type is
    obj.target_type
    """
    resolver_type = f"release-{obj.target_type.value}"
    resolver = get_node_resolver(resolver_type)
    return resolver(obj, info, **kw)()


@query.field("directory")
def directory_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.directory.DirectoryNode:
    resolver = get_node_resolver("directory")
    return resolver(obj, info, **kw)()


@directory_entry.field("target")
def directory_entry_target_resolver(
    obj: rs.directory_entry.DirectoryEntryNode, info: GraphQLResolveInfo, **kw
):
    """
    directory entry target can be a directory or a content
    """
    resolver_type = f"dir-entry-{obj.type}"
    resolver = get_node_resolver(resolver_type)
    return resolver(obj, info, **kw)()


@query.field("content")
def content_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.content.ContentNode:
    resolver = get_node_resolver("content")
    return resolver(obj, info, **kw)()


# Connection resolvers
# A connection resolver should return an instance of BaseConnection


@query.field("origins")
def origins_resolver(
    obj: None, info: GraphQLResolveInfo, **kw
) -> rs.origin.OriginConnection:
    resolver = get_connection_resolver("origins")
    return resolver(obj, info, **kw)()


@origin.field("visits")
def visits_resolver(
    obj: rs.origin.OriginNode, info: GraphQLResolveInfo, **kw
) -> rs.visit.OriginVisitConnection:
    resolver = get_connection_resolver("origin-visits")
    return resolver(obj, info, **kw)()


@origin.field("snapshots")
def origin_snapshots_resolver(
    obj: rs.origin.OriginNode, info: GraphQLResolveInfo, **kw
) -> rs.snapshot.OriginSnapshotConnection:
    """ """
    resolver = get_connection_resolver("origin-snapshots")
    return resolver(obj, info, **kw)()


@visit.field("status")
def visitstatus_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.visit_status.VisitStatusConnection:
    resolver = get_connection_resolver("visit-status")
    return resolver(obj, info, **kw)()


@snapshot.field("branches")
def snapshot_branches_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.snapshot_branch.SnapshotBranchConnection:
    resolver = get_connection_resolver("snapshot-branches")
    return resolver(obj, info, **kw)()


@revision.field("parents")
def revision_parents_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.revision.ParentRevisionConnection:
    resolver = get_connection_resolver("revision-parents")
    return resolver(obj, info, **kw)()


# @revision.field("revisionLog")
# def revision_log_resolver(obj, info, **kw):
#     resolver = get_connection_resolver("revision-log")
#     return resolver(obj, info, **kw)()


@directory.field("entries")
def directory_entry_resolver(
    obj, info: GraphQLResolveInfo, **kw
) -> rs.directory_entry.DirectoryEntryConnection:
    resolver = get_connection_resolver("directory-entries")
    return resolver(obj, info, **kw)()


# Any other type of resolver


@release_target.type_resolver
@directory_entry_target.type_resolver
@branch_target.type_resolver
def union_resolver(obj, *_) -> str:
    """
    Generic resolver for all the union types
    """
    return obj.is_type_of()
