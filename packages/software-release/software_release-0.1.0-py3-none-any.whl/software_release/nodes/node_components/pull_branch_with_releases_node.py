from software_release.nodes.node import Node


@Node.register_as_subclass('pull-branch-with-releases')
class PullBranchWithReleasesNode(Node):

    @classmethod
    def _handle(cls, request):
        current_branch: str = request.repository.current_branch.name
        branch_to_pull = request.branch_holding_releases

        request.repository.repo_proxy.git.checkout(branch_to_pull)

        request.repository.repo_proxy.git.pull()

        cls.run(cls.command('render', 'pulled-branch-msg',
            request.repository.directory_path,
            branch_to_pull,
            'origin',
            'ssh',
            [_ for _ in request.repository.repo_proxy.remote().urls]))

        request.repository.repo_proxy.git.checkout(current_branch)

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
