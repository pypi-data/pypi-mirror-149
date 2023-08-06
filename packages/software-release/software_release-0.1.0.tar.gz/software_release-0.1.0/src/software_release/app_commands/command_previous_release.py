from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.previous_release import PreviousReleased


__all__ = ['PreviousVersionCommand']


class AbstractPreviousVersionCommand(BaseCommand):

    def __new__(cls, commit_receiver: PreviousReleased, repository):
        return super().__new__(cls, commit_receiver, 'compute_previous_release', repository)


@CommandClass.register_as_subclass('previous-release')
class PreviousVersionCommand(AbstractPreviousVersionCommand):

    def __new__(cls, repository):
        return super().__new__(cls, PreviousReleased(), repository)
