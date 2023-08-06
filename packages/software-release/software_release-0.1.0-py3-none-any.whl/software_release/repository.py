import attr

from .repository_interface import RepositoryInterface
from .head_interface import HeadInterface


@attr.s
class Repository(RepositoryInterface):
    _active_branch: HeadInterface = attr.ib()
    _directory_path: str = attr.ib()
    _repo_proxy = attr.ib()
    _org_name: str = attr.ib()
    _name: str = attr.ib()  # represents name on github.com
    _github_proxy = attr.ib()

    @property
    def active_branch(self) -> HeadInterface:
        return self._active_branch

    @property
    def current_branch(self) -> HeadInterface:
        return self.repo_proxy.active_branch

    @property
    def directory_path(self) -> str:
        return self._directory_path

    @property
    def repo_proxy(self):
        return self._repo_proxy

    @property
    def org_name(self) -> str:
        return self._org_name

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def github_proxy(self):
        return self._github_proxy
