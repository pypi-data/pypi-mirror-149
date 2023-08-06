from .git_pull_interface import PullerInterface


class GitPuller(PullerInterface):

    def pull(self, repository, reference=None, **kwargs):
        remote_server_name_slug = 'origin'
        remote = repository.repo_proxy.remote(name=remote_server_name_slug)
        remote.pull(reference)
        self.remote_slug = remote_server_name_slug
        self.urls = [_ for _ in remote.urls]
