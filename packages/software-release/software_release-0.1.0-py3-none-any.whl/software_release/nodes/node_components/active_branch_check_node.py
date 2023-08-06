from software_release.nodes.node import Node
import sys


@Node.register_as_subclass('active-branch-check')
class ActiveBranchCheckNode(Node):

    @classmethod
    def _handle(cls, request):
        is_release_branch = cls.run(cls.command('check-branches', request.repository))
        if is_release_branch:
            cls.run(cls.command('render', 'release-branch-msg', request.repository.active_branch.name))
        else:
            cls.run(cls.command('render', 'no-release-branch-msg', request.repository.active_branch.name))
            cls.run(cls.command('render',
                'Please navigate to the local repository, checkout a \'release\' branch and rerun the wizard'))
        return is_release_branch

    def handle(self, request):
        is_release_branch = self._handle(request)
        if is_release_branch:
            return super().handle(request)
        else:
            sys.exit(1)
