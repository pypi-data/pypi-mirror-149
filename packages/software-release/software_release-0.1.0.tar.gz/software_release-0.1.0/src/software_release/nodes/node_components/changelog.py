from datetime import date

from git import exc
from software_release.nodes.node import Node

import logging

logger = logging.getLogger(__name__)

@Node.register_as_subclass('changelog')
class UpdateChangelogNode(Node):

    @classmethod
    def _handle(cls, request):
        today = date.today()
        current_date = today.strftime('%Y-%m-%d')

        command = cls.command('update-changelog', request.repository,
            request.previous_version, request.new_version, current_date)
        changelog_file, changes_added = cls.run(command)
        if changes_added:
            try:
                command = cls.command('render', 'updated-changelog',
                    request.repository.directory_path, changelog_file, changes_added)
                cls.run(command)
            except Exception as error:
                logger.error(str(error))
                cls.run(cls.command('render',
                    "Updated CHANGELOG\n"
                    "Changes:\n" + str(changes_added)
                ))

            # Commit changes; git commit -m "..."
            commit_message = f'docs: update changelog with the release\'s changes'
            command = cls.command('commit-changes', request.repository, commit_message)
            commit = cls.run(command)

            try:
                command = cls.command('render', 'commited-files',
                    request.repository.directory_path, [changelog_file], commit.message, commit.sha)
                cls.run(command)
            except Exception as error:
                logger.error(str(error))
                cls.run(cls.command('render',
                    "Updated CHANGELOG\n"
                    "Changes:\n" + str(changes_added)
                ))

        request.changelog_additions = changes_added

    def handle(self, request):
        self._handle(request)
        return super().handle(request)
