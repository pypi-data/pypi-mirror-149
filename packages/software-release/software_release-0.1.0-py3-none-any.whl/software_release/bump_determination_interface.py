from abc import ABC
from .version_bump_type import BumpType


class BumpComputerInterface(ABC):

    def compute_bump(self, commits: list) -> BumpType:
        raise NotImplementedError
