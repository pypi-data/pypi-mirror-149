from .command_interface import CommandInterface


class CommandHistory:
    """The global command history is just a stack; supports 'push' and 'pop' methods."""
    def __init__(self):
        self._history = []

    def push(self, command: CommandInterface):
        self._history.append(command)

    def pop(self) -> CommandInterface:
        return self._history.pop(0)

    @property
    def stack(self):
        return self._history


class Invoker:
    """A class that simply executes a command and pushes it into its internal command history stack.

    Args:
        history (CommandHistory): the command history object which acts as a stack
    """
    history: CommandHistory
    def __init__(self, *args):
        if not args:
            self.history = CommandHistory()
        else:
            self.history = args[0]

    def execute_command(self, command: CommandInterface):
        response = command.execute()
        self.history.push(command)
        return response