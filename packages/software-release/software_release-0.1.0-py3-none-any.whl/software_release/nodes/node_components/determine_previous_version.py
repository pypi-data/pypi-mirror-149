from software_release.nodes.node import Node
from software_release.version_class import VersionString


@Node.register_as_subclass('prev-version')
class DeterminePreviousVersionNode(Node):

    @classmethod
    def _handle(cls, request):
        
        # Simple detection of release by looking at git tags on master branch
        command = cls.command('previous-release', request.repository)
        previous_version = cls.run(command)

        # If no previous release found, show a message
        if previous_version == '0.0.0':
            command = cls.command('render', 'no-release-tag-found')
            cls.run(command)

            command = cls.command('render',
                f'\nIt seems this is the first ever semantic release we are about to make!\n',
                ' We assume that the previously release version is 0.0.0 for the purpose',
                'of automatically recommending the next release version.\n',
            )
            cls.run(command)
        else:  # previous release found, show a message
            command = cls.command('render', 'release-tag-found', previous_version)
            cls.run(command)

        return previous_version

    def handle(self, request):
        previous_version = self._handle(request)
        request.previous_version = previous_version
        return super().handle(request)
