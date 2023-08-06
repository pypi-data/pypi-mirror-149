import copy
from .base_command import BaseCommand


class PrototypeCommand(BaseCommand):
    """An runnable/executable Command that acts as a prototype through the 'copy' python magic function.

    When a command instance is invoked with 'copy', the receiver is copied explicitly in a shallow way. The rest of the
    command arguments are assumed to be performance invariant (eg it is not expensive to copy the 'method' attribute,
    which is a string) and are handled automatically.
    """
    def __copy__(self):
        _ = type(self)(copy.copy(self._receiver), self._method)
        _.append_arg(*self._args)
        return _
