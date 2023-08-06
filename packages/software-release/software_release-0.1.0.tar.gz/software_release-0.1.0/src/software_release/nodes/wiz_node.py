from software_patterns import SubclassRegistry
from software_release.commands import command_factory, Invoker
from software_release.visual_components.dialogs.interactive_dialog import Dialog

invoker = Invoker

class NodeWithCommand(SubclassRegistry):

    def run(cls, command):
        return invoker.execute_command(command)

    def command(cls, command_type: str, *args):
        return command_factory.construct(command_type, *args)

    def dialog(cls, dialog_type, **kwargs):
        return Dialog.create(dialog_type, **kwargs)



class NodeWithCommand:
    @classmethod
    def run(cls, command):
        return invoker.execute_command(command)
    @classmethod
    def command(cls, command_type: str, *args):
        return command_factory.construct(command_type, *args)
    @classmethod
    def dialog(cls, dialog_type, **kwargs):
        return Dialog.create(dialog_type, **kwargs)
