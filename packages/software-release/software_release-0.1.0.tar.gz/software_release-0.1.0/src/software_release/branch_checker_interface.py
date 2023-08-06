from typing import Any

from .branch_interface import BranchInterface


class BranchCheckerInterface:
    """Interface that can return the active branch of a repository."""
    
    def active_branch(self, repository: Any) -> BranchInterface:
        raise NotImplementedError

    def is_release_branch(self, branch: Any) -> bool:
        raise NotImplementedError
