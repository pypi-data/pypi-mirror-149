import attr

from .command_factory_interface import CommandFactoryInterface
from .command_class import CommandClass



@attr.s
class CommandFactory(CommandFactoryInterface):

    def construct(self, *args, **kwargs):
        return CommandClass.create(*args, **kwargs)
