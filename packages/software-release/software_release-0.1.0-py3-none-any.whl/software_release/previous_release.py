import re
from typing import Optional

import attr
from git import TagObject


class PreviousReleasedVersionComputerInterface:

    def compute_previous_release(self, repository):
        raise NotImplementedError


@attr.s
class PreviousReleased(PreviousReleasedVersionComputerInterface):
    revision: attr.ib()

    def compute_previous_release(self, repository) -> Optional[str]:
        """Find the latest release version, assuming all releases are git tagged with vX.Y.Z.

        Find the latest release version, by looking at the tags in the git history for a given
        git repository.

        It is assumed, that all releases have been git tagged with a simple semantic release
        pattern vMAJOR.MINOR.PATCH (no patterns for pre-release, builds, supported yet).

        WARNING: tags not matching the v\d+\.\d+\.\d+ regular expression shall be skipped!

        In case there is no git tag matching the above criteria, then it is assumed that the
        project is about to make its first ever release and hence the '0.0.0' string is
        returned.

        Args:
            repository (software_release.repository.Repository): the repository get a release
                from

        Returns:
            (Optional[str]): the semantic version string or None if no matching tag was found
        """
        return get_last_version(repository.repo_proxy, skip_tags=None)


def get_last_version(repo, skip_tags=None) -> Optional[str]:
    """Find the latest version released by scanning the repo tags.

    The repo tags need to start with v;

    Example: v1.0.0, v0.5.1, etc

    :return: A string containing a version number.
    """
    skip_tags = skip_tags or []

    def version_finder(tag):
        if isinstance(tag.commit, TagObject):
            return tag.tag.tagged_date
        return tag.commit.committed_date

    for i in sorted(repo.tags, reverse=True, key=version_finder):
        if re.match(r"v\d+\.\d+\.\d+", i.name):  # Matches vX.X.X
            if i.name in skip_tags:
                continue
            return i.name[1:]  # Strip off 'v'
