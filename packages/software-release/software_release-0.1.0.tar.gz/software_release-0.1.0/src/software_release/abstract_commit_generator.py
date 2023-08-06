from .commit_generator_interface import CommitGeneratorInterface
from .repository_interface import RepositoryInterface


class AbstractCommitGenerator(CommitGeneratorInterface):
    
    def __init__(self, repository: RepositoryInterface, from_commit) -> None:
        self.repository = repository
        self.from_commit = from_commit

    def __iter__(self):
        return iter(self.generate_commits(self.repository, self.from_commit))
