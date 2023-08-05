from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Type

from swh.graphql.utils import utils

from .base_node import BaseNode


@dataclass
class PageInfo:
    hasNextPage: bool
    endCursor: str


class BaseConnection(ABC):
    """
    Base class for all the connection resolvers
    """

    _node_class: Optional[Type[BaseNode]] = None
    _page_size = 50  # default page size

    def __init__(self, obj, info, paged_data=None, **kwargs):
        self.obj = obj
        self.info = info
        self.kwargs = kwargs
        self._paged_data = paged_data

    def __call__(self, *args, **kw):
        return self

    @property
    def edges(self):
        return self._get_edges()

    @property
    def nodes(self):
        """
        Override if needed; return a list of objects

        If a node class is set, return a list of its (Node) instances
        else a list of raw results
        """
        if self._node_class is not None:
            return [
                self._node_class(self.obj, self.info, node_data=result, **self.kwargs)
                for result in self.get_paged_data().results
            ]
        return self.get_paged_data().results

    @property
    def pageInfo(self):  # To support the schema naming convention
        # FIXME, add more details like startCursor
        return PageInfo(
            hasNextPage=bool(self.get_paged_data().next_page_token),
            endCursor=utils.get_encoded_cursor(self.get_paged_data().next_page_token),
        )

    @property
    def totalCount(self):  # To support the schema naming convention
        return self._get_total_count()

    def _get_total_count(self):
        """
        Will be None for most of the connections
        override if needed/possible
        """
        return None

    def get_paged_data(self):
        """
        Cache to avoid multiple calls to
        the backend (_get_paged_result)
        return a PagedResult object
        """
        if self._paged_data is None:
            # FIXME, make this call async (not for v1)
            self._paged_data = self._get_paged_result()
        return self._paged_data

    @abstractmethod
    def _get_paged_result(self):
        """
        Override for desired behaviour
        return a PagedResult object
        """
        # FIXME, make this call async (not for v1)
        return None

    def _get_edges(self):
        # FIXME, make cursor work per item
        # Cursor can't be None here
        return [{"cursor": "dummy", "node": node} for node in self.nodes]

    def _get_after_arg(self):
        """
        Return the decoded next page token
        override to use a specific token
        """
        return utils.get_decoded_cursor(self.kwargs.get("after"))

    def _get_first_arg(self):
        """
        page_size is set to 50 by default
        """
        return self.kwargs.get("first", self._page_size)
