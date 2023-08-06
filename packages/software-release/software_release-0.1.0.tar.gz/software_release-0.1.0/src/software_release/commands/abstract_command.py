from abc import ABC
from .command_interface import CommandInterface


class AbstractCommand(CommandInterface, ABC):
    """An abstract implementation of the CommandInterface.

    The assumption is that the command involves a main 'receiver' object.
    Commands of this type follow the receiver.method(*args) pattern/model.
    The receiver object usually is commonly acting as an 'oracle' on the
    application or on the situation/context.

    Args:
        receiver (object): usually holds the callback function/code with the business logic
    """
    def __new__(cls, receiver):
        cmd_instance = super().__new__(cls)
        cmd_instance._receiver = receiver
        return cmd_instance
