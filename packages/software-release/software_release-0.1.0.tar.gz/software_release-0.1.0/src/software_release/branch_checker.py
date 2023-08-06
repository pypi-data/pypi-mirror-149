from .branch_checker_interface import BranchCheckerInterface
from .repository_interface import RepositoryInterface

from .branch_interface import BranchInterface


class BranchChecker(BranchCheckerInterface):

    def active_branch(self, repository: RepositoryInterface) -> BranchInterface:
        return repository.active_branch

    def is_release_branch(self, branch: BranchInterface) -> bool:
        return branch.name.startswith('release')
