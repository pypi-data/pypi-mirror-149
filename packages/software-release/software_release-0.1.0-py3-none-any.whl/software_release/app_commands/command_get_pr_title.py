from abc import ABC
from typing import Any
from software_release.commands.command_class import CommandClass
from software_release.commands.base_command import BaseCommand
from software_patterns import SubclassRegistry


class PullRequestTitleBuilderInterface(ABC):

    def build_title(self, request: Any) -> str:
        raise NotImplementedError


class PullRequestTitleBuilder(metaclass=SubclassRegistry[PullRequestTitleBuilderInterface]):
    pass


@PullRequestTitleBuilder.register_as_subclass('base')
class BasePullRequestTitleBuilder(PullRequestTitleBuilderInterface):

    def build_title(self, request: Any) -> str:
        pull_request_title = getattr(request, 'pull_request_title', '')
        if pull_request_title:
            return str(pull_request_title)
        return '{title} {version} Release'.format(
            title=' '.join([x[0].upper() + x[1:] for x in request.repository.name.split('-')]),
            version=f'v{request.new_version}'
        )


class AbstractBuildPullRequestTitleCommand(BaseCommand):

    def __new__(cls, receiver: PullRequestTitleBuilderInterface, request):
        return super().__new__(cls, receiver, 'build_title', request)

    # def __new__(cls, *args):
    #     return super().__new__(cls, PullRequestTitleBuilder.create('base'), 'build_title', *args)


@CommandClass.register_as_subclass('build-pr-title')
class BuildPullRequestTitle(AbstractBuildPullRequestTitleCommand):
    def __new__(cls, request, infer_title='base'):
        return super().__new__(cls, PullRequestTitleBuilder.create(infer_title), request)
