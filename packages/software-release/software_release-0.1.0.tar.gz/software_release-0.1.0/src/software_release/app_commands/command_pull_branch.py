from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand

from software_release.git_pull import GitPuller



class AbstractPullBranchCommand(BaseCommand):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, GitPuller(), 'pull', *args, **kwargs)


@CommandClass.register_as_subclass('pull-branch')
class PullBranchCommand(AbstractPullBranchCommand):
    
    def execute(self) -> None:
        super().execute()
        remote_server_name_slug = self._receiver.remote_slug
        remote_urls = self._receiver.urls
        return remote_server_name_slug, remote_urls
