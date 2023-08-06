
from software_release.nodes.node import Node
from software_release.version_class import VersionString


@Node.register_as_subclass('version-bump')
class VersionBumpNode(Node):

    @classmethod
    def _handle(cls, request):
        
        # change files on disk
        command = cls.command('update-version-string', request.repository,
            request.previous_version, request.new_version)
        updated_files = cls.run(command)

        # Commit changes; git commit -m "..."
        if updated_files:
            command = cls.command('render', 'updated-version-string', request.repository.directory_path, updated_files)
            cls.run(command)

            commit_message = f'release(semantic_version): bump version to {request.new_version}'
            command = cls.command('commit-changes', request.repository, commit_message)
            commit = cls.run(command)

            command = cls.command('render', 'commited-files',
                request.repository.directory_path, updated_files, commit.message, commit.sha)
            cls.run(command)


    def handle(self, request):
        self._handle(request)
        return super().handle(request)
