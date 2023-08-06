from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """Stand-alone command, encapsulating all logic and data needed."""

    @abstractmethod
    def execute(self) -> any:
        """Execute the command; run the command's logic."""
        raise NotImplementedError
