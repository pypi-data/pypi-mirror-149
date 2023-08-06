from abc import ABC, abstractmethod


class TaggerInterface(ABC):
    """Tag a commit on a local repository."""
    
    @abstractmethod
    def tag_commit(self, repository, tag, reference=None, **kwargs):
        """Tag the current HEAD or a commit if reference is given."""
        raise NotImplementedError
