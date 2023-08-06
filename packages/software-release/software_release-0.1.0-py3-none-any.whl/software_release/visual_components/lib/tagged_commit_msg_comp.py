import attr

from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('tagged-commit-msg')
class TaggedCommitMessageComponent(VisualComponent):
    tag_name: str = attr.ib()
    path: str = attr.ib()
    commit_sha: str = attr.ib()
    message: str = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.message == None:
            self.message = ''
        else:
            self.message = f" with message '{self.message}'"

    def render(self):
        return [
            f'GIT TAG\n --> Tag {self.tag_name} ({self.path}){self.message} commit {self.commit_sha}\n',
        ]
