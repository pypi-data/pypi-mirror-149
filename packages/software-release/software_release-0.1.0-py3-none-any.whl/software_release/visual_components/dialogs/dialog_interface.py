from abc import ABC, abstractmethod


class TerminalDialogInterface(ABC):
    """Ask for input through the terminal, with an interactive dialog.

    Implement this interface to provide class instances with the 'dialog'
    method, which receives input though the terminal by using an interactive
    dialog (ie input dialog, radio button dialog, etc).
    """

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
