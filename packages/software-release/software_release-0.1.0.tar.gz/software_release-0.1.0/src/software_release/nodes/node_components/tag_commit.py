from software_release.nodes.node import Node


@Node.register_as_subclass('tag-commit-on-branch-with-releases')
class TagHeadCommitNode(Node):

    @classmethod
    def _handle(cls, request):
        tag_string = f'v{str(request.new_version)}'
        message=None
        tag_reference = cls.run(cls.command(
            'git-tag',
            request.repository,
            tag_string,
            reference=request.branch_holding_releases,
            message=message
        ))

        cls.run(cls.command('render', 'tagged-commit-msg',
            tag_string,
            str(tag_reference.path),
            str(tag_reference.object),
            message
        ))

        # print(str(tag_reference.name))  # v1.1.0
        # print(str(tag_reference.path))  # refs/tags/v1.1.0
        # print(str(tag_reference.object))   # 067c0cdcc71d179aaeaac739dccdc75ea2174f65
        # print(str(tag_reference.tag.message))  # 'DEL-ME'
        # print(str(tag_reference.tag.type))  # 'tag'

        return tag_reference

    def handle(self, request):
        tag_reference = self._handle(request)
        request.tag_reference = tag_reference
        return super().handle(request)
