import re

from .version_determination import PreviousReleasedVersionComputerInterface
from .repository_interface import RepositoryInterface


SEMANTIC_VERSION = \
    r'\d+\.\d+(?:\.\d+(?:[\-\._]?\w(?:\.\d+)(?:[\-\._]\w(?:\.\d+))))?'

VERSION_STRING_REG_EX = fr'v?({SEMANTIC_VERSION})'


class ReleaseFinderByTag(PreviousReleasedVersionComputerInterface):

    def compute_previous_release(self, repository: RepositoryInterface):
        # scan master branch from most recent and return first git tag that
        # matches regex v?{\d}+
        master_branch = repository.branch('master')
        commits_generator = iter(master_branch)
        for commit in commits_generator:
            match = re.match(VERSION_STRING_REG_EX, commit.tag)
            if match:
                return match.group(1)


# class ReleaseFinderFromSourceCode(PreviousReleasedVersionComputerInterface):

#     def compute_previous_release(self, repository):
        # scan pyproject -> setup.cfg
        # determine file where version is hard coded
        # determine regex to use
        # extract hard coded version string
        # return version string