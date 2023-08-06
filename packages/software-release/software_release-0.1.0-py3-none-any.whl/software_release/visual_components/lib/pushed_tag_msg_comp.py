import attr

from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('pushed-tag-msg')
class PushedActiveBranchComponent(VisualComponent):
    tag_name: str = attr.ib()
    remote_slug: str = attr.ib(default='origin')

    def render(self):
        return [
            f'\nGIT PUSH: Pushed Tag \'{self.tag_name}\' to remote \'{self.remote_slug}\' !\n\n',
        ]
