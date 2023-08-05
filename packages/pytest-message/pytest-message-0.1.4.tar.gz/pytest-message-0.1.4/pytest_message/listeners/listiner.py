import abc
from typing import Any


class Listener(abc.ABC):
    @abc.abstractmethod
    def update(self, data: Any) -> None:
        """Updates it's state after notify event"""

    @abc.abstractmethod
    def finish(self) -> None:
        """Ends notify process. Sends notification to service"""
