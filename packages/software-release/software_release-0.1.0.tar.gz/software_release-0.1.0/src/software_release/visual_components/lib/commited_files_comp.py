import os
from typing import List
import attr
from ..visual_component import VisualComponent


__all__ = ['CommitedFiles']


@attr.s
@VisualComponent.register_as_subclass('commited-files')
class CommitedFiles(VisualComponent):
    repository_dir: str = attr.ib()
    full_paths: List[str] = attr.ib()
    commit_message = attr.ib()
    commit_hexsha = attr.ib()
    
    _relative_paths: List[str] = attr.ib(init=False,
        default=attr.Factory(lambda self: [os.path.relpath(path, self.repository_dir) for path in self.full_paths], takes_self=True))
    string_lines = attr.ib(init=False,
        default=attr.Factory(lambda self: [f' * {f}' for f in self._relative_paths], takes_self=True))

    def __attrs_post_init__(self):
        self.MESSAGE = f'Commited changes !'
        self.MSG1 = f'Commit message: {self.commit_message}'
        self.MSG2 = f'Commit hexsha: {self.commit_hexsha}'
        self._LEN = max([len(x) for x in self.string_lines] + [
            len(self.MESSAGE),
            len(self.MSG1),
            len(self.MSG2),
        ])
        self.HEADER = '-' * self._LEN

    def render(self):
        return [
            f'\n{self.MESSAGE}\n',
            f'{self.MSG1}\n',
            f'{self.MSG2}\n',
            f'{self.HEADER}\n',
            '\n'.join(self.string_lines) + '\n',
        ]
