from software_release.nodes.node import Node


@Node.register_as_subclass('branch-references')
class BranchReferencesUpdateNode(Node):
    
    @classmethod
    def _handle(cls, request):
        # Update files on disk
        BRANCH = 'master'
        command = cls.command('update-branch-refs', request.repository, BRANCH)
        updated_files = cls.run(command)

        # Commit files
        if updated_files:
            command = cls.command('render', 'updated-branch-refs', request.repository.directory_path, updated_files, BRANCH)
            cls.run(command)

            # Commit changes; git commit -m "..."
            commit_message = f'docs: update branch references to point to {BRANCH} branch'
            command = cls.command('commit-changes', request.repository, commit_message)
            commit = cls.run(command)

            command = cls.command('render', 'commited-files',
                request.repository.directory_path, updated_files, commit.message, commit.sha)
            cls.run(command)

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
