
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand

from software_release.push_active_branch import ActiveBranchPusher



__all__ = ['PushActiveBranchCommand']


class AbstractPushBranchCommand(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, ActiveBranchPusher(), 'push', *args)


@CommandClass.register_as_subclass('push-active-branch')
class PushActiveBranchCommand(AbstractPushBranchCommand):
    
    def execute(self) -> None:
        super().execute()
        remote_server_name_slug = self._receiver.remote_slug
        remote_urls = self._receiver.urls
        return remote_server_name_slug, remote_urls
