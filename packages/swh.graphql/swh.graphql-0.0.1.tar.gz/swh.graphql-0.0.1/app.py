from ariadne import gql, load_schema_from_path, make_executable_schema

from swh.graphql.resolvers import resolvers, scalars

type_defs = gql(load_schema_from_path("swh/graphql/schema/schema.graphql"))

schema = make_executable_schema(
    type_defs,
    resolvers.query,
    resolvers.origin,
    resolvers.visit,
    resolvers.visit_status,
    resolvers.snapshot,
    resolvers.snapshot_branch,
    resolvers.revision,
    resolvers.release,
    resolvers.directory,
    resolvers.directory_entry,
    resolvers.branch_target,
    resolvers.release_target,
    resolvers.directory_entry_target,
    scalars.id_scalar,
    scalars.string_scalar,
    scalars.datetime_scalar,
    scalars.swhid_scalar,
    scalars.hash_value_scalar,
)
