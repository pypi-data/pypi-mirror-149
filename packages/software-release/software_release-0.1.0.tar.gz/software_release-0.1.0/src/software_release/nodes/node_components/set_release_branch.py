from software_release.nodes.node import Node

@Node.register_as_subclass('set-release-branch')
class SetReleaseBranchNode(Node):

    def __init__(self, branch_name: str) -> None:
        super().__init__()
        self._branch_name = str(branch_name)

    def handle(self, request):
        request.branch_holding_releases = self._branch_name
        return super().handle(request)
