from ariadne.wsgi import GraphQL

from .app import schema

application = GraphQL(schema)
