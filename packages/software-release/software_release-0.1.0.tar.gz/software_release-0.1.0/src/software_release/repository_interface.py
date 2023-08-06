from typing import Generator, Protocol
from .head_interface import HeadInterface
from .branch_interface import BranchInterface


class RepositoryInterface(Protocol):
    active_branch: HeadInterface
    directory_path: str

    def branch(self, branch_name: str) -> BranchInterface: ...

    def iter_commits(self, revision: str = None) -> Generator: ...
