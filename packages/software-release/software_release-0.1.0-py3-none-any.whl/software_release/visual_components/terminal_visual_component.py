from typing import List


class TerminalVisualComponent:

    def render(self) -> List[str]:
        raise NotImplementedError

    def __str__(self) -> str:
        return ''.join(self.render())
