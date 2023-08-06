import attr
from typing import List

from .git_status_interface import GitStatusInterface


@attr.s
class GitStatus(GitStatusInterface):
    _modified: List[str] = attr.ib()
    _untracked: List[str] = attr.ib()

    @property
    def modified(self) -> List[str]:
        return self._modified

    @property
    def untracked(self) -> List[str]:
        return self._untracked

    @classmethod
    def from_repo(cls, repository):
        changed_files = [
            item.a_path for item in repository.repo_proxy.index.diff(None)
        ]
        untracked_files = [file for file in changed_files
            if file in repository.repo_proxy.untracked_files]
        
        return GitStatus(
            sorted(list(set(changed_files).difference(set(untracked_files)))),
            sorted(untracked_files)
        )
