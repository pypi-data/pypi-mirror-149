# import pkg_resources
import os
from pathlib import Path

from ariadne import gql, load_schema_from_path, make_executable_schema

from .resolvers import resolvers, scalars

type_defs = gql(
    # pkg_resources.resource_string("swh.graphql", "schem/schema.graphql").decode()
    load_schema_from_path(
        os.path.join(Path(__file__).parent.resolve(), "schema", "schema.graphql")
    )
)

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
