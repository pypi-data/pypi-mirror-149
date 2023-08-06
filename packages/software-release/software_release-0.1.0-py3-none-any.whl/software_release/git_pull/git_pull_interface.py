from abc import ABC, abstractmethod


class PullerInterface(ABC):
    """Pull a branch from a remote repository to a local."""
    
    @abstractmethod
    def pull(self, repository, reference=None, **kwargs):
        """Pull the currently active branch or a branch from the remote."""
        raise NotImplementedError
