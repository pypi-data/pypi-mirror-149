
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand


class AbstractPushTagCommand(BaseCommand):

    def __new__(cls, repository, tag_reference):
        return super().__new__(cls, cls.push_tag, '__call__', repository, tag_reference)


@CommandClass.register_as_subclass('push-tag')
class PushTagCommand(AbstractPushTagCommand):

    @staticmethod
    def push_tag(repository, tag_reference):
        repository.repo_proxy.remotes.origin.push(tag_reference)
