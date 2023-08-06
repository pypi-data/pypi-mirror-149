from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.commit_interface import Commiter
from software_release.git_status_factory import GitStatusFactory


__all__ = ['CommitChangesCommand']


class AbstractCommitChangesCommand(BaseCommand):

    def __new__(cls, commit_receiver: Commiter, repository, commit_message: str, files: list):
        return super().__new__(cls, commit_receiver, 'commit', repository, commit_message, files)



@CommandClass.register_as_subclass('commit-changes')
class CommitChangesCommand(AbstractCommitChangesCommand):

    def __new__(cls, repository, commit_message: str):
        git_status = GitStatusFactory.create(repository)
        changed_files = git_status.modified
        return super().__new__(cls, Commiter(), repository, commit_message,
            changed_files)
