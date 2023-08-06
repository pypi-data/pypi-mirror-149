import attr
from .check_branches_cor import CheckBranchesCoR


@attr.s
class CheckBranchesNode:
    cor = attr.ib(default=attr.Factory(CheckBranchesCoR))

    def run(self, request):
        return self.cor.handle(request)


