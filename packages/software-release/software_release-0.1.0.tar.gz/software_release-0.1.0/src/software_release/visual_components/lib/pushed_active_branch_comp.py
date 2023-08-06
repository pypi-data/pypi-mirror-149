import attr

from ..visual_component import VisualComponent


__all__ = ['PushedActiveBranchComponent']


@attr.s
@VisualComponent.register_as_subclass('pushed-active-branch')
class PushedActiveBranchComponent(VisualComponent):
    local_repo_dir_path: str = attr.ib()
    branch_name: str = attr.ib()
    remote_slug: str = attr.ib()
    protocol: str = attr.ib()
    urls: str = attr.ib()

    def __attrs_post_init__(self):
        self.LOCAL = 'Local'
        self.REMOTE = 'Remote'
        self.ARROW = '-->'
        self.WEB = 'Internet'
        self.COMP = f'{self.ARROW} {self.protocol} {self.ARROW} {self.WEB} {self.ARROW}'
        
        self.LOC_MACHINE = f'\'{self.branch_name}\' ({self.LOCAL.lower()})'
        self.REM_SERVER = f'\'{self.branch_name}\' ({self.remote_slug})'

        self.local = f'[{self.LOCAL}]'
        # assuming len(self.local) < len(self.LOC_MACHINE) set self.local_offset
        self.local_offset = int(len(self.LOC_MACHINE) / 2 - len(self.local) / 2)

        self.remote = f'[{self.REMOTE}]'
        # assuming len(self.remote) < len(self.REM_SERVER) set self.rem_offset
        self.rem_offset = int(len(self.REM_SERVER) / 2 - len(self.remote) / 2)

        self.labels_max_len = max((len(self.LOCAL), len(self.REMOTE)))
        self.space = ' ' * ( max(( len(self.LOC_MACHINE), len(self.local) )) - len(self.local) + len(self.COMP) - self.local_offset + self.rem_offset)

    def render(self):
        return [
            f'\nGIT PUSH: Pushed Active branch \'{self.branch_name}\' to remote \'{self.remote_slug}\' !\n\n',
            
            f' {self.LOCAL}{" " * (self.labels_max_len - len(self.LOCAL))}: {self.local_repo_dir_path}\n',
            f' {self.REMOTE}{" " * (self.labels_max_len - len(self.REMOTE))}: {", ".join(self.urls)}\n\n',
            
            f' {" " * self.local_offset}{self.local} {self.space} {self.remote}\n'
            f' {self.LOC_MACHINE} {self.COMP} {self.REM_SERVER}'
        ]
