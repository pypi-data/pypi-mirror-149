import attr

from ..visual_component import VisualComponent


__all__ = ['NoReleaseTagFoundComponent']


@attr.s
@VisualComponent.register_as_subclass('no-release-tag-found')
class NoReleaseTagFoundComponent(VisualComponent):

    def render(self):
        return [
            f'\nTagged commit NOT found.\n',
            'We can assume that this is the first release we are making!'
        ]
