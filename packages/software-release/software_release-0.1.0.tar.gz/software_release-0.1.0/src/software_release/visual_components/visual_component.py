from software_patterns import SubclassRegistry
from .terminal_visual_component import TerminalVisualComponent


class VisualComponent(TerminalVisualComponent, metaclass=SubclassRegistry): pass
