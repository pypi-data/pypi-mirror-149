from ..interactive_dialog import Dialog


@Dialog.register_as_subclass('press-enter-to-continue')
class PressEnterToContinueDialog(Dialog):

    def dialog(self, data):
        input("Press Enter to continue...")
