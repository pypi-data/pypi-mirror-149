from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand

from software_release.git_tag import GitTagger


class AbstractGitTagCommand(BaseCommand):

    def __new__(cls, repository, tag, reference=None, **kwargs):
        return super().__new__(cls, GitTagger(), 'tag_commit',
            repository, tag, reference=reference, **kwargs)


@CommandClass.register_as_subclass('git-tag')
class GitTagCommand(AbstractGitTagCommand):
    pass