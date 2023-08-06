import re
from typing import Optional

from software_release.commit_generator import BranchCommitsGenerator
from software_release.version_determination import NextVersionComputerInterface
from software_release.angular_parser import parse_commit_message, \
    UnknownCommitMessageStyleError


class NextVersionComputer(NextVersionComputerInterface):

    def recommend_next_version(self, repository, current_version, version=None):
        level_bump = evaluate_version_bump(
            str(current_version),
            BranchCommitsGenerator(repository, f'v{current_version}' if bool(current_version) else current_version),
            force=version
        )

        return current_version + level_bump, level_bump

        # TODO Clean: remove comments
        # if not level_bump:
        #     return current_version, 

        # new_version = current_version + level_bump
        # return new_version, level_bump

    # def get_revision(self, ref:Optional[str] = None) -> str:
    #     """Construct a revision string from the given ref.

    #     Ref can be a branch name, a commit sha or a tag.

    #     If reg is None, constructs a revision based on the first ever commit.

    #     Args:
    #         ref (str, optional): the reference name to a git object. Defaults to
    #             None.

    #     Returns:
    #         str: the git revision string
    #     """
    #     if not bool(ref):
    #         return 'HEAD'
    #     return f'...{ref}'


LEVELS = {
    1: "patch",
    2: "minor",
    3: "major",
}

CHANGELOG_SECTIONS = [
    'feature',
    'fix',
    'test',
    'breaking',
    'documentation',
    'performance',
    'ci',
]

re_breaking = re.compile('BREAKING CHANGE: (.*)')


def evaluate_version_bump(current_version: str, commit_generator, force: str = None) -> Optional[str]:
    """
    Read git log since the last release to decide if we should make a major, minor or patch release.

    :param current_version: A string with the current version number.
    :param force: A string with the bump level that should be forced.
    :return: A string with either major, minor or patch if there should be a release.
             If no release is necessary, None will be returned.
    """
    if force:
        return force

    bump = None

    changes = []
    commit_count = 0

    # for _hash, commit_message in get_commit_log("v{0}".format(current_version)):
    for commit in iter(commit_generator):
        commit_message = commit.message
        if commit_message.startswith(str(current_version)):
            # Stop once we reach the current version
            # (we are looping in the order of newest -> oldest)

            break

        commit_count += 1

        # Attempt to parse this commit using the currently-configured parser
        try:
            message = parse_commit_message(commit_message)
            changes.append(message.bump)
        except UnknownCommitMessageStyleError as err:
            pass

    if changes:
        # Select the largest required bump level from the commits we parsed
        level = max(changes)
        if level in LEVELS:
            bump = LEVELS[level]

    # if commit_count > 0 and bump is None:
    #     bump = "patch"

    return bump
