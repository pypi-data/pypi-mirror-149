import attr

from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('no-release-branch-msg')
class ReleaseBranchNotFoundComponent(VisualComponent):
    branch_name: str = attr.ib()

    def render(self):
        return [
            f'\nActive branch name \'{self.branch_name}\' indicates it is NOT '
            'a \'Release\' Branch\n'
            'Please checkout a branch with name starting with \'release\''
            ' and re-run the cli.\n',
        ]
