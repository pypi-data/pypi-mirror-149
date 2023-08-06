from software_release.nodes.node import Node


@Node.register_as_subclass('welcome-to-wizard-node')
class WelcomeToReleaseWizardNode(Node):

    @classmethod
    def _handle(cls, request):
        cmd = cls.command('render',
            'Welcome to the Interactive Release Wizard !\n',
            "we will go step-by-step all the actions required to 'release' a new version of your software",
        )
        cls.run(cmd)
        cls.dialog('press-enter-to-continue').dialog(None)
        cmd = cls.command('render-repo-info', request.repository)
        return cls.run(cmd)

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
