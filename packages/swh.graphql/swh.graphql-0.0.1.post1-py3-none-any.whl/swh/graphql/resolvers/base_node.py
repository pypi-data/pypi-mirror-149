from abc import ABC
from collections import namedtuple

from swh.graphql.errors import ObjectNotFoundError


class BaseNode(ABC):
    """
    Base class for all the Node resolvers
    """

    def __init__(self, obj, info, node_data=None, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs
        self._node = self._get_node(node_data)
        # handle the errors, if any, after _node is set
        self._handle_node_errors()

    def _get_node(self, node_data):
        """
        Get the node object from the given data
        if the data (node_data) is none make
        a function call to get data from backend
        """
        if node_data is None:
            node_data = self._get_node_data()
        return self._get_node_from_data(node_data)

    def _get_node_from_data(self, node_data):
        """
        Get the object from node_data
        In case of a dict, convert it to an object
        Override to support different data structures
        """
        if type(node_data) is dict:
            return namedtuple("NodeObj", node_data.keys())(*node_data.values())
        return node_data

    def _handle_node_errors(self):
        """
        Handle any error related to node data

        raise an error in case the object returned is None
        override for specific behaviour
        """
        if self._node is None:
            raise ObjectNotFoundError("Requested object is not available")

    def __call__(self, *args, **kw):
        return self

    def _get_node_data(self):
        """
        Override for desired behaviour
        This will be called only when
        node_data is None
        """
        # FIXME, make this call async (not for v1)
        return None

    def __getattr__(self, name):
        """
        Any property defined in the sub-class
        will get precedence over the _node attributes
        """
        return getattr(self._node, name)

    def is_type_of(self):
        return self.__class__.__name__


class BaseSWHNode(BaseNode):
    @property
    def SWHID(self):
        return self._node.swhid()
