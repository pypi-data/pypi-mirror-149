import attr

from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('active-branch')
class ActiveBranchComponent(VisualComponent):
    branch_name: str = attr.ib()

    def __attrs_post_init__(self):
        self.ACTIVE_BRANCH_MSG = 'Active Branch'
        self.STYLE_LINE_1 = '-' * len(self.ACTIVE_BRANCH_MSG)

    def render(self):
        return [
            f'{self.ACTIVE_BRANCH_MSG}: {self.branch_name}\n',
            self.STYLE_LINE_1,
        ]
