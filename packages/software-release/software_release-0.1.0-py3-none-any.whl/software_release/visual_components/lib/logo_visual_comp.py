
from ..visual_component import VisualComponent


@VisualComponent.register_as_subclass('logo')
class Logo(VisualComponent):
    text = 'Software Release v0.5'
    line = '#' * len(text)

    def render(self):
        return [
            '##' + self.line + '##\n',
            '# ' + self.text + ' #\n',
            '##' + self.line + '##',
        ]
