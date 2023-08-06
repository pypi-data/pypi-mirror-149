import attr

from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('release-branch-msg')
class ReleaseBranchFoundComponent(VisualComponent):
    branch_name: str = attr.ib()

    def render(self):
        return [
            f'\nActive branch name \'{self.branch_name}\' indicates it is a \'Release\' Branch'
            '\nWe proceed!',
        ]
