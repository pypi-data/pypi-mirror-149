from typing import Optional, Type, TypeVar
from software_release import repository

from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_release.pull_request import PullRequest

import logging

logger = logging.getLogger(__name__)


_T = TypeVar('_T')


@CommandClass.register_as_subclass('find-pr')
class FindGithubPullRequestCommand(BaseCommand):

    def __new__(cls: Type[_T], request):
        return super().__new__(cls, cls.find_pull_request, '__call__', request)

    @classmethod
    def find_pull_request(cls, request) -> Optional[PullRequest]:
        try:
            gh_pull_request = cls._get_github_pull_request(request)
            return PullRequest.from_github_pull_request(gh_pull_request)
        except PullRequestNotFound:
            return None

    @classmethod
    def _get_github_pull_request(cls, request):

        # get OPEN pull requests as paginated list
        # (it should be just one in this case, since head and base specify a
        # singular Pull Request
        paginated_list = request.repository.github_proxy.get_repo(
            f'{request.repository.org_name}/{request.repository.name}').get_pulls(
            head=request.repository.current_branch.name,
            base=request.branch_holding_releases,
        )

        pull_requests_list = [p for p in paginated_list]
        
        github_pull_request = pull_requests_list[0]

        if len(pull_requests_list) != 1:
            logger.error("Pull Requests List has more than one elements!")

        return github_pull_request

    @classmethod
    def iter_pulls(cls, paginated_list):
        """Iterate over the Github Pull Requests within a Paginated List."""
        page_index = 0
        pull_request_list = paginated_list.get_page(page_index)
        while pull_request_list:
            for github_pull_request in pull_request_list:
                yield github_pull_request
            page_index += 1
            pull_request_list = paginated_list.get_page(page_index)


class PullRequestNotFound(Exception):
    pass
