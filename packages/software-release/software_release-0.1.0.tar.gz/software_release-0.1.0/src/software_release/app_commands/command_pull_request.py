import os
import re

from github import Github
from github.GithubException import GithubException
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.pull_request import PullRequest


__all__ = ['OpenPullRequest']


class AbstractPullRequest(BaseCommand):

    def __new__(cls, *args):
        return super().__new__(cls, cls.create_pull_request, '__call__', *args)


@CommandClass.register_as_subclass('pull-request')
class OpenPullRequest(AbstractPullRequest):

    @staticmethod
    def create_pull_request(owner, repo_name, title, description, head_branch, base_branch):

        # using an access token
        try:
            g = Github(os.environ['GH_TOKEN'])
        except KeyError as error:
            raise MissingGithubTokenError("The GH_TOKEN environment variable was not found") from error
        repo = g.get_repo(f"{owner}/{repo_name}")

        lines = list(description.split('\n'))
        prev_line = lines[0]
        for i in range(1, len(lines)):
            line = lines[i]
            if re.match(r'^\^{2,}', line):
                lines[i] = '-' * len(prev_line)
            prev_line = lines[i]

        try:
            pr = repo.create_pull(
                title=title,
                body='\n'.join(lines),
                head=str(head_branch),
                base=str(base_branch)
            )
        except GithubException as error:
            raise PullRequestCreationError("Failed to create a new Pull Request"
            " on github.com! Could be that there is an already opened PR,"
            " with the same 'from' and 'to' branches.") from error
        return PullRequest.from_github_pull_request(pr)


class PullRequestCreationError(Exception): pass

class MissingGithubTokenError(Exception): pass
