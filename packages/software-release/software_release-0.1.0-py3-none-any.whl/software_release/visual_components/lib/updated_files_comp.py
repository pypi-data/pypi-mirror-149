import os
from typing import List
import attr
from ..visual_component import VisualComponent


__all__ = ['UpdatedVersionStringFiles', 'UpdatedBranchReferences']


@attr.s
@VisualComponent.register_as_subclass('updated-version-string')
class UpdatedVersionStringFiles(VisualComponent):
    repository_dir: str = attr.ib()
    full_paths: List[str] = attr.ib()
    
    _relative_paths: List[str] = attr.ib(init=False,
        default=attr.Factory(lambda self: [os.path.relpath(path, self.repository_dir) for path in self.full_paths], takes_self=True))
    string_lines = attr.ib(init=False,
        default=attr.Factory(lambda self: [f' * {f}' for f in self._relative_paths], takes_self=True))

    def __attrs_post_init__(self):
        self.MESSAGE = 'Updated references of the version string!'
        self.UPDATE_MSG_HEADER = 'Updated files:'
        self._LEN = max([len(x) for x in self.string_lines] + [len(self.MESSAGE)])
        self.HEADER = '\\' + '_' * self._LEN + '/'
        self.FOOTER = '/' + '-' * self._LEN + '\\'

    def render(self):
        return [
            f'\n{self.HEADER}\n',
            f'{self.MESSAGE}\n',
            f'{self.UPDATE_MSG_HEADER}\n',
            '\n'.join(self.string_lines) + '\n',
            self.FOOTER
        ]



@attr.s
@VisualComponent.register_as_subclass('updated-branch-refs')
class UpdatedBranchReferences(VisualComponent):
    repository_dir: str = attr.ib()
    full_paths: List[str] = attr.ib()
    branch_name: str = attr.ib()

    _relative_paths: List[str] = attr.ib(init=False,
        default=attr.Factory(lambda self: [os.path.relpath(path, self.repository_dir) for path in self.full_paths], takes_self=True))
    string_lines = attr.ib(init=False,
        default=attr.Factory(lambda self: [f'  * {f}' for f in self._relative_paths], takes_self=True))

    def __attrs_post_init__(self):
        self.MESSAGE = f'Updated branch references to point to the {self.branch_name} branch !'
        self.UPDATE_MSG_HEADER = ' Updated files:'
        self._LEN = max([len(x) for x in self.string_lines] + [len(self.MESSAGE)])
        self.HEADER = '\\' + '_' * self._LEN + '/'
        self.FOOTER = '/' + '-' * self._LEN + '\\'

    def render(self):
        return [
            f'\n{self.HEADER}\n',
            f'{self.MESSAGE}\n',
            f'{self.UPDATE_MSG_HEADER}\n',
            '\n'.join(self.string_lines) + '\n',
            self.FOOTER
        ]




@attr.s
@VisualComponent.register_as_subclass('updated-changelog')
class UpdatedChangelog(VisualComponent):
    repository_dir: str = attr.ib()
    changelog_file: str = attr.ib()
    changes_added = attr.ib()

    _relative_path: str = attr.ib(init=False,
        default=attr.Factory(lambda self: os.path.relpath(self.changelog_file, self.repository_dir), takes_self=True))
    string_line = attr.ib(init=False,
        default=attr.Factory(lambda self: f'  * {self._relative_path}', takes_self=True))

    def __attrs_post_init__(self):
        self.MESSAGE = f'Updated {self._relative_path} with the release\'s changes !'
        self.HEADER = 'CONTENT ADDED'
        self._LEN = max([len(x) for x in self.changes_added.split('\n')])
        self._LEN_REM = self._LEN - 2 - len(self.HEADER)
        self._LEN_1 = int(self._LEN_REM / 2)
        self._LEN_2 = self._LEN_REM - self._LEN_1
        self.HEADER = '\\' + '_' * self._LEN_1 + self.HEADER + '_' * self._LEN_2 + '/'
        self.FOOTER = '/' + '-' * (self._LEN - 2) + '\\'

    def render(self):
        return [
            f'\n{self.MESSAGE}\n',
            f'\n{self.HEADER}\n',
            self.changes_added,
            f'\n{self.FOOTER}',
        ]
