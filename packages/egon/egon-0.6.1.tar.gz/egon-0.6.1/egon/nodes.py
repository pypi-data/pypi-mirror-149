"""The ``nodes`` module supports the construction of individual pipeline nodes.
``Source``, ``Node``,  and ``Target`` classes are provided for creating nodes
that produce, analyze, and consume data respectively.
"""

from __future__ import annotations

import abc
from abc import ABC
from itertools import chain
from typing import Collection
from typing import List, Tuple, Union

from . import connectors, exceptions
from .multiprocessing import MPool


def _get_nodes_from_connectors(connector_list: Collection[connectors.BaseConnector]) -> Tuple:
    """Return the parent nodes from a list of ``Connector`` objects
    
    Args:
        connector_list: The connectors to get parents of
        
    Returns:
        A list of node instances
    """

    return tuple(p.parent_node for c in connector_list for p in c.partners)


class AbstractNode(abc.ABC):
    """Base class for constructing pipeline nodes"""

    def __init__(self, name: str = None, num_processes: int = 1) -> None:
        """Represents a single pipeline node"""

        self._pool: MPool = MPool(num_processes, self._target)
        self._allow_pool_overwrite = True  # See setter for ``num_processes`` attribute
        self.name = name or self.__class__.__name__

        # Accumulate all attributes that are Input or Output types
        self._inputs = []
        self._outputs = []
        for connector in self._get_attrs(connectors.BaseConnector):
            connector._node = self  # Make the connector aware of its parent node
            if isinstance(connector, connectors.Input):
                self._inputs.append(connector)

            else:  # Assume all other connectors are outputs
                self._outputs.append(connector)

        self._inputs = tuple(self._inputs)
        self._outputs = tuple(self._outputs)

    def _get_attrs(self, attr_type=None) -> List:
        """Return a list of instance attributes matching the given type

        All class attributes are ignored.

        Args:
            attr_type: The object type to search for

        Returns:
            A list of attributes with type ``attr_type``
        """

        attr_list = []
        ignore = dir(self.__class__)

        for attr_name in dir(self):
            if (not attr_name.startswith('_')) and (attr_name not in ignore):
                attr = getattr(self, attr_name)
                if isinstance(attr, attr_type):
                    attr_list.append(attr)

        return attr_list

    @property
    def num_processes(self) -> int:
        """The number of processes assigned to the pool"""

        return self._pool.num_processes

    @num_processes.setter
    def num_processes(self, val) -> None:
        if not self._allow_pool_overwrite:
            raise RuntimeError('Cannot change number of processes on running or finished node')

        self._pool = MPool(val, self._target)

    @property
    def connectors(self) -> Tuple[Tuple[connectors.Input, ...], Tuple[connectors.Output, ...]]:
        """Return tuples with all input and output connectors associated with the node

        Returns:
            A tuple of Input connectors and a tuple of Output connectors
        """

        return self._inputs, self._outputs

    @property
    def upstream_nodes(self) -> Tuple[Union[Source, Node]]:
        """Returns a list of nodes that are upstream from the current node"""

        return _get_nodes_from_connectors(self._get_attrs(connectors.Input))

    @property
    def downstream_nodes(self) -> Tuple[Union[Node, Target]]:
        """Returns a list of nodes that are downstream from the current node"""

        return _get_nodes_from_connectors(self._get_attrs(connectors.Output))

    @abc.abstractmethod
    def validate(self) -> None:
        """Raise an exception if the node object was constructed improperly

        Raises:
            ValueError: For an invalid instance construction
        """

    def _validate_connections(self) -> None:
        """Raise an exception if any of the node's Inputs/Outputs are missing connections

        Raises:
            MissingConnectionError: For an invalid instance construction
        """

        for conn in chain(*self.connectors):
            if not conn.is_connected():
                raise exceptions.MissingConnectionError(
                    f'Connector {conn} does not have an established connection (Node: {conn.parent_node})')

    @abc.abstractmethod
    def action(self) -> None:
        """The primary analysis task performed by this node"""

    def setup(self) -> None:
        """Setup tasks called before running ``action``"""

    def teardown(self) -> None:
        """Teardown tasks called after running ``action``"""

    def _target(self) -> None:
        """Entry point for running the node in a multiprocessing pool"""

        self._allow_pool_overwrite = False
        self.setup()
        self.action()
        self.teardown()

    def execute(self):
        """Execute the pipeline node

        Execution includes all ``setup``, ``action``, and ``teardown`` tasks.
        """

        self._pool.start()
        self._pool.join()

    def is_finished(self) -> bool:
        """Return whether all node processes have finished processing data

        The returned value defaults to ``True`` when the number of processes
        assigned to the node instance is zero.
        """

        return self._pool.is_finished()

    def is_expecting_data(self) -> bool:
        """Return whether the node is still expecting data from upstream

        This function includes checks for whether any upstream nodes are still
        running or any data is pending in the queue of an input connector.
        """

        for input_connector in self._get_attrs(connectors.Input):
            # IMPORTANT: The order of the following code blocks is crucial
            # We check for any running upstream nodes first
            for output_connector in input_connector.partners:
                if not output_connector.parent_node.is_finished():
                    return True

            # Check for any unprocessed data once we know there are no
            # nodes still populating any input queues
            if not input_connector.is_empty():
                return True

        return False

    def __str__(self) -> str:  # pragma: no cover
        return f'<{self.__repr__()} object at {hex(id(self))}>'

    def __repr__(self) -> str:  # pragma: no cover
        return f'{self.__class__.__name__}(num_processes={self.num_processes})'


class Source(AbstractNode, ABC):
    """A pipeline process that only has output streams"""

    def validate(self) -> None:
        """Raise exception if the object is not a valid instance

        Raises:
            MalformedSourceError: For an invalid instance construction
            OrphanedNodeError: For an instance that is inaccessible by connectors
        """

        if self._get_attrs(connectors.Input):
            raise exceptions.MalformedSourceError('Source objects cannot have upstream components.')

        if not self._get_attrs(connectors.Output):
            raise exceptions.OrphanedNodeError('Source has no output connectors and is inaccessible by the pipeline.')

        self._validate_connections()


class Target(AbstractNode, ABC):
    """A pipeline process that only has input streams"""

    def validate(self) -> None:
        """Raise exception if the object is not a valid instance

        Raises:
            MalformedTargetError: For an invalid instance construction
            OrphanedNodeError: For an instance that is inaccessible by connectors
        """

        if self._get_attrs(connectors.Output):
            raise exceptions.MalformedTargetError('Source objects cannot have upstream components.')

        if not self._get_attrs(connectors.Input):
            raise exceptions.OrphanedNodeError('Target has no input connectors and is inaccessible by the pipeline.')

        self._validate_connections()


class Node(AbstractNode, ABC):
    """A pipeline process that can have any number of input or output streams"""

    def validate(self) -> None:
        """Raise exception if the object is not a valid instance

        Raises:
            OrphanedNodeError: For an instance that is inaccessible by connectors
        """

        inputs, outputs = self.connectors
        if not (inputs or outputs):
            raise exceptions.OrphanedNodeError('Node has no associated connectors and is inaccessible by the pipeline.')

        self._validate_connections()
