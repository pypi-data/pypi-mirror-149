from ariadne.asgi import GraphQL

from app import schema

application = GraphQL(schema, debug=True)
