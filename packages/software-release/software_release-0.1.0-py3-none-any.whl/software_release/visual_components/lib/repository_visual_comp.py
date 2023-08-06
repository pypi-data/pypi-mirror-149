import attr
from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('repository')
class RepositoryComponent(VisualComponent):
    line = '-'
    text = 'Git Repository'

    directory_path: str = attr.ib()

    def render(self):
        return [
            f'{self.text}: {self.directory_path}',
            '\n',
            self.line * len(self.text)
        ]
