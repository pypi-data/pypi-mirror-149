import attr
from abc import abstractmethod
from software_patterns import SubclassRegistry
from .dialog_interface import TerminalDialogInterface


@attr.s
class TerminalDialog:
    config: dict = attr.ib(default={})


    @abstractmethod
    def dialog(self, data):
        """Receive input though the terminal, using an interactive dialog.

        All required information for rendering the dialog (ie text, available 
        choices, etc) should should be included in the 'data' method argument.

        Args:
            data (dict): information required for rendering the content of the
            dialog
        """
        raise NotImplementedError


class Dialog(TerminalDialog, metaclass=SubclassRegistry): pass
