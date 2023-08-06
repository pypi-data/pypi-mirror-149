from software_release.nodes.node import Node


@Node.register_as_subclass('welcome-to-app')
class WelcomeToAppMessageNode(Node):

    @classmethod
    def _handle(cls):
        cmd = cls.command('render-logo')
        return cls.run(cmd)

    def handle(self, request):
        self._handle()
        return super().handle(request)
