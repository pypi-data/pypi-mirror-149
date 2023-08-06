import sys
from software_release.nodes.node import Node
from software_release.pull_request import PullRequest
from software_release.app_commands.command_pull_request import (
    MissingGithubTokenError,
    PullRequestCreationError,
    PullRequest,
)

import logging

logger = logging.getLogger(__name__)

@Node.register_as_subclass('open-pull-request')
class OpenPullRequestNode(Node):

    @classmethod
    def _handle(cls, request):

        BRANCH_WITH_CHANGES = request.repository.active_branch.name
        DESTINATION_BRANCH = 'master'
        title = cls.run(cls.command('build-pr-title', request))

        command = cls.command('pull-request',
            request.repository.org_name,
            request.repository.name,
            title,
            # f"Software Patterns v{request.new_version} Release", # title
            request.changelog_additions, # description
            BRANCH_WITH_CHANGES, # head_branch, where our changes are implemented
            DESTINATION_BRANCH, # base_branch, where we want to merge to
        )

        try:
            pull_request = cls.run(command)
            cls.run(cls.command('render', 'created-pull-request',
                pull_request.number,
                pull_request.url,
                pull_request.html_url,
                BRANCH_WITH_CHANGES,
                DESTINATION_BRANCH
            ))
        except MissingGithubTokenError as error:
            print(error)
            print('Sorry, you have to restart and set the GH_TOKEN correctly.')
            sys.exit(1)
        except PullRequestCreationError as github_pr_creation_error:
            if getattr(request, 'accept_existing_pr', False):
                # try:
                pull_request = cls.cmd('find-pr', request)

                cls.echo("Found an already opened 'Release' Pull Request: "
                    "{from_branch} -> {to_branch}\n url: {url}\n html_url: {html_url}".format(
                        from_branch=BRANCH_WITH_CHANGES,
                        to_branch=DESTINATION_BRANCH,
                        url='',
                        html_url=''
                    ) + "\n\nContinuing!")
                # except Exception as github_pr_get_error:
                #     print(f"Unfortunately, we could not create a new"
                #     "Pull Request on github.com. Exception:\n {github_pr_creation_error}")
                #     print(f"Unfortunately, we could not either find a matching "
                #     "Pull Request, already opened on github.com. Exception:\n {github_pr_get_error}")
                #     print('Exiting ..')
                #     sys.exit(1)
            else:
                print(github_pr_creation_error)
                print('Probably a Pull Request already exists, with the same target'
                    ' and destination branches. Sorry, but there is a "release" '
                    'already under way!\nExiting ..')
                sys.exit(1)

        return pull_request

    def handle(self, request):
        # TODO make sure flag is correct !
        request.accept_existing_pr = True
        request.pull_request = self._handle(request)
        return super().handle(request)
