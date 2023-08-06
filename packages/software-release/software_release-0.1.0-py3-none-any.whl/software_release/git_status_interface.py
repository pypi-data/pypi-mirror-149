from abc import ABC, abstractmethod
from typing import List


class GitStatusInterface(ABC):

    @property
    @abstractmethod
    def modified(self) -> List[str]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def untracked(self) -> List[str]:
        raise NotImplementedError
