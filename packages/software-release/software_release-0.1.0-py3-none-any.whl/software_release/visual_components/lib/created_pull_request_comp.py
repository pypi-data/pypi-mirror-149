import attr

from ..visual_component import VisualComponent


__all__ = ['CreatedPullRequest']


@attr.s
@VisualComponent.register_as_subclass('created-pull-request')
class CreatedPullRequest(VisualComponent):
    number: str = attr.ib()
    api_url: str = attr.ib()
    url: str = attr.ib()
    from_branch = attr.ib()
    to_branch = attr.ib()

    def render(self):
        return [
            f'\nPULL REQUEST: Opened Pull Request with number {self.number} on github !\n\n',
            
            f' url    : {self.url}\n',
            f' api_url: {self.api_url}\n\n',

            f' Requesting to merge {self.from_branch} --> {self.to_branch}'
        ]
