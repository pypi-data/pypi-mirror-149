from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.new_release import NextVersionComputer


__all__ = ['NewVersionCommand']


class AbstractNewVersionCommand(BaseCommand):

    def __new__(cls, receiver: NextVersionComputer, repository, current_version, force_version):
        return super().__new__(cls, receiver, 'recommend_next_version',
            repository,
            current_version,
            force_version
        )


@CommandClass.register_as_subclass('new-release')
class NewVersionCommand(AbstractNewVersionCommand):

    def __new__(cls, repository, current_version, force_version=None):
        return super().__new__(cls, NextVersionComputer(), repository, current_version, force_version)
