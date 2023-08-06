from software_release.nodes.node import Node


@Node.register_as_subclass('push-tag')
class PushTagNode(Node):

    @classmethod
    def _handle(cls, request):
        cls.run(cls.command(
            'push-tag',
            request.repository,
            request.tag_reference,
        ))

        cls.run(cls.command('render', 'pushed-tag-msg',
            request.tag_reference.name,
        ))


    def handle(self, request):
        self._handle(request)
        return super().handle(request)
