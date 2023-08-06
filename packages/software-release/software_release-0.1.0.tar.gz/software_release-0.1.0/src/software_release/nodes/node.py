
from software_patterns.subclass_registry import SubclassRegistry
# from .wiz_node import NodeWithCommand
from software_release.handler.handler import Handler
from software_patterns import SubclassRegistry

from software_release.commands import command_factory, Invoker
from software_release.visual_components.dialogs.interactive_dialog import Dialog

invoker = Invoker()


# class NodeWithCommand(SubclassRegistry):

#     def run(cls, command):
#         return invoker.execute_command(command)

#     def command(cls, command_type: str, *args):
#         return command_factory.construct(command_type, *args)

#     def dialog(cls, dialog_type, **kwargs):
#         return Dialog.create(dialog_type, **kwargs)



class Node(metaclass=SubclassRegistry):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    def handle(self, request) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None

    @classmethod
    def run(cls, command):
        return invoker.execute_command(command)

    @classmethod
    def command(cls, command_type: str, *args, **kwargs):
        return command_factory.construct(command_type, *args, **kwargs)

    @classmethod
    def dialog(cls, dialog_type, **kwargs):
        return Dialog.create(dialog_type, **kwargs)

    @classmethod
    def echo(cls, data: str):
        return cls.run(cls.command('render', data))

    @classmethod
    def cmd(cls, command_type: str, *args, **kwargs):
        """Build and Run a Command. Shortcut method to execute commands."""
        return cls.run(cls.command(command_type, *args, **kwargs))