from .command_class import CommandClass
from .prototype_command import PrototypeCommand


@CommandClass.register_as_subclass('Command')
class Command(PrototypeCommand): pass
