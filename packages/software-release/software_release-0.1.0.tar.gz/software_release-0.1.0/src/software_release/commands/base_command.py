from .abstract_command import AbstractCommand


class BaseCommand(AbstractCommand):
    """A concrete implementation of the Abstract Command.

    This command simply invokes a 'method' on the 'receiver'. When constructing
    instances of BaseCommand make sure you respect the 'method' signature. For
    that, you can use the *args to provide the receiver's method arguments.

    Intuitively, what happens is

    .. code-block:: python

        receiver.method(*args)

    and that is another way to show how the *args are passed to method

    Args:
        receiver (object): an object that is actually executing/receiving the command; usually holds the callback
        function/code
        method (str): the name of the receiver's method to call (it has to be callable and to exist on the receiver)
    """
    def __new__(cls, receiver, method: str, *args, **kwargs):
        base_cmd_instance = super().__new__(cls, receiver)
        base_cmd_instance._method = method
        base_cmd_instance._args = list(args)  # this is a list that can be minimally be []
        base_cmd_instance._kwargs = kwargs  # this dict can minimaly be {}
        return base_cmd_instance

    def append_arg(self, *args):
        self._args.extend(args)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args_list):
        self._args = list(args_list)

    def execute(self) -> None:
        return getattr(self._receiver, self._method)(*self._args, **self._kwargs)
