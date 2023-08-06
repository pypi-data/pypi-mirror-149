from abc import ABC, abstractmethod
from software_release.commands.command_class import CommandClass
from software_release.commands.abstract_command import AbstractCommand
from software_release.repository_interface import RepositoryInterface


__all__ = ['CheckBranchesCommand', 'SleepCommand']


class AbstractNodeCommand(AbstractCommand, ABC):

    def execute(self) -> any:
        return getattr(self._receiver, self.method)(*self.args)

from software_release.branch_checker import BranchChecker


@CommandClass.register_as_subclass('check-branches')
class CheckBranchesCommand(AbstractNodeCommand):

    def __new__(cls, repository: RepositoryInterface):
        cmd_instance = super().__new__(cls, BranchChecker())
        cmd_instance.method = 'is_release_branch'
        cmd_instance.args = [repository.active_branch]
        return cmd_instance


from time import sleep

@CommandClass.register_as_subclass('sleep')
class SleepCommand(AbstractNodeCommand):

    def __new__(cls, seconds_duration: float):
        cmd_instance = super().__new__(cls, sleep)
        cmd_instance.method = '__call__'
        cmd_instance.args = [seconds_duration]
        return cmd_instance


@CommandClass.register_as_subclass('update-code')
class UpdateCodeCommand(AbstractNodeCommand):
    def __new__(cls, repository: RepositoryInterface):
        pass