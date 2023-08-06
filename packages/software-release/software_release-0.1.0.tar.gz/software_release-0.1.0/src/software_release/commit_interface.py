from __future__ import annotations
from abc import ABC, abstractmethod


class CommitInterface(ABC):
    """Represents a commit object."""    
    
    @property
    @abstractmethod
    def message(self) -> str:
        """The message associated with the commit."""
        raise NotImplementedError

    @property
    @abstractmethod
    def sha(self) -> str:
        """The unique hash sha key associated with the commit."""
        raise NotImplementedError


class CommitFactoryInterface:

    def create(self, *args, **kwargs) -> CommitInterface:
        raise NotImplementedError

    def new(self, *args, **kwargs) -> CommitInterface:
        raise NotImplementedError



import attr

@attr.s(slots=True, frozen=True)
class CommitObject(CommitInterface):
    _sha = attr.ib()
    _message = attr.ib()

    @property
    def message(self) -> str:
        return self._message
    
    @property
    def sha(self) -> str:
        return self._sha


class CommiterInterface(ABC):

    @abstractmethod
    def commit(self, *args, **kwargs):
        raise NotImplementedError


@attr.s
class Commiter(CommiterInterface):
    commit_factory: CommitFactoryInterface = attr.ib(default=attr.Factory(lambda: CommitFactory))

    def commit(self, repository, commit_message: str, files: list, **kwargs) -> CommitInterface:
        new_commit = self.commit_factory.new(repository, commit_message, files, **kwargs)
        return new_commit

from typing import Protocol


class PythonGitCommit(Protocol):
    name_rev: str
    message: str


class CommitFactory(CommitFactoryInterface):
    
    @classmethod
    def from_git_commit(cls, git_commit: PythonGitCommit):
        return cls.create(git_commit.hexsha, git_commit.message)

    @classmethod
    def create(cls, *args, **kwargs):
        return CommitObject(*args, **kwargs)
    
    @classmethod
    def new(cls, *args, **kwargs) -> CommitInterface:
        repository: str = args[0]
        commit_message: str = args[1]
        files: list = args[2]
        repository.repo_proxy.index.add(files)
        git_commit = repository.repo_proxy.index.commit(commit_message)
        return cls.from_git_commit(git_commit)
