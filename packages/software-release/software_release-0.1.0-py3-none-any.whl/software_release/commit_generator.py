from typing import Optional
from .abstract_commit_generator import AbstractCommitGenerator
from software_release.commit_interface import CommitFactory


__all__ = ['BranchCommitsGenerator']


def get_revision(ref:Optional[str] = None) -> str:
    """Construct a revision string from the given ref.

    Ref can be a branch name, a commit sha or a tag.

    If reg is None, constructs a revision based on the first ever commit.

    Args:
        ref (str, optional): the reference name to a git object. Defaults to
            None.

    Returns:
        str: the git revision string
    """
    if not bool(ref):
        return 'HEAD'
    return f'...{ref}'


class BranchCommitsGenerator(AbstractCommitGenerator):
    """Generator yielding the commit history of a branch based on the given revision."""

    def generate_commits(self, repository, revision):
        revision = get_revision(revision)
        print(' -> REVISION to generate commits:', str(revision))
        for git_commit in repository.repo_proxy.iter_commits(str(revision)):
            yield CommitFactory.from_git_commit(git_commit)
