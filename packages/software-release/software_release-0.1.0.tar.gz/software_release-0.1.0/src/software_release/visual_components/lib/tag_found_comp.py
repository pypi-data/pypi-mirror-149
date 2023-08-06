import attr

from ..visual_component import VisualComponent


__all__ = ['ReleaseTagFoundComponent']


@attr.s
@VisualComponent.register_as_subclass('release-tag-found')
class ReleaseTagFoundComponent(VisualComponent):
    release_version = attr.ib()

    def render(self):
        return [
            f'\nTagged commit found with version {self.release_version} !'
        ]
