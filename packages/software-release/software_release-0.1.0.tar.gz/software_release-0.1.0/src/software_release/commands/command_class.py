from software_patterns import SubclassRegistry
from .command_interface import CommandInterface


__all__ = ['CommandClass']


class CommandClass(metaclass=SubclassRegistry[CommandInterface]): pass
