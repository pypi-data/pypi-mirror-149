"""The ``mock`` module defines prebuilt pipeline nodes for developing
unittests. Instead of accomplishing a user defined action, mock nodes sleep
for a pre-defined number of seconds.
"""

from abc import ABC
from typing import Optional

from egon import nodes
from egon.connectors import Input, Output
from egon.nodes import AbstractNode


class MockObject(AbstractNode, ABC):
    """Base class for mock testing nodes"""

    def __init__(self, name: Optional[str] = None) -> None:
        self._is_finished = False
        super(MockObject, self).__init__(name=name)

    def is_finished(self) -> bool:
        """Return whether the mock node has already been executed"""

        return self._is_finished

    def execute(self) -> None:
        """Execute the mock pipeline node"""

        super(MockObject, self)._target()
        self._is_finished = True


class MockSource(MockObject, nodes.Source):
    """A ``Source`` subclass that implements placeholder functions for abstract methods"""

    def __init__(self, load_data: list = None, name: Optional[str] = None) -> None:
        self.output = Output()
        self.load_data = load_data or []
        super(MockSource, self).__init__(name)

    def action(self) -> None:
        """Placeholder function to satisfy requirements of abstract parent"""

        for x in self.load_data:
            self.output.put(x)


class MockTarget(MockObject, nodes.Target):
    """A ``Target`` subclass that implements placeholder functions for abstract methods"""

    def __init__(self, name: Optional[str] = None) -> None:
        self.input = Input()
        self.accumulated_data = []
        super(MockTarget, self).__init__(name)

    def action(self) -> None:
        """Placeholder function to satisfy requirements of abstract parent"""

        for x in self.input.iter_get():
            self.accumulated_data.append(x)


class MockNode(MockObject, nodes.Node):
    """A ``Node`` subclass that implements placeholder functions for abstract methods"""

    def __init__(self, name: Optional[str] = None) -> None:
        self.output = Output()
        self.input = Input()
        super(MockNode, self).__init__(name)

    def action(self) -> None:  # pragma: no cover
        """Placeholder function to satisfy requirements of abstract parent"""

        for x in self.input.iter_get():
            self.output.put(x)
