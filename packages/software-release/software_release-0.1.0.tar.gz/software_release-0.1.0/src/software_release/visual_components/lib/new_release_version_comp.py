import attr

from ..visual_component import VisualComponent


__all__ = ['NewReleaseVersion']


@attr.s
@VisualComponent.register_as_subclass('new-release-version')
class NewReleaseVersion(VisualComponent):
    release_version: str = attr.ib()

    def __attrs_post_init__(self):
        self.MESSAGE = f'New Release Version {self.release_version} !'
        self._LEN = len(self.MESSAGE) + 4
        self.HEADER = '-' * self._LEN
        self.FOOTER = '-' * self._LEN

    def render(self):
        return [
            f'\n{self.HEADER}\n',
            f'| {self.MESSAGE} |\n',
            f'{self.FOOTER}',
        ]
