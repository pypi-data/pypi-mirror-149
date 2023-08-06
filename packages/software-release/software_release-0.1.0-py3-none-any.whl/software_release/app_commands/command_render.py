from abc import ABC, abstractmethod
from software_release.commands.command_class import CommandClass
from software_release.commands.abstract_command import AbstractCommand

from software_release.component_renderer import ComponentRenderer

from software_release.visual_components import VisualComponent


__all__ = ['RenderLogo', 'RenderRepository', 'RenderActiveBranch']


command_renderer = ComponentRenderer()


def discover_visual_component(component_representation: str, *args):
    if component_representation in VisualComponent.subclasses:
        return VisualComponent.create(component_representation, *args)
    return '\n'.join([component_representation] + list(args))


class AbstractRenderCommand(AbstractCommand):
    def __new__(cls, receiver, *properties):
        render_cmd_instance = super().__new__(cls, receiver)
        render_cmd_instance.props = properties
        return render_cmd_instance

    def execute(self) -> any:
        return self._receiver.render(self.visual_components)


@CommandClass.register_as_subclass('render')
class RenderCommand(AbstractRenderCommand):
    def __new__(cls, *components):
        render_cmd_instance = super().__new__(cls, command_renderer)
        render_cmd_instance.visual_components = [discover_visual_component(*components)]
        return render_cmd_instance


@CommandClass.register_as_subclass('render-logo')
class RenderLogo(AbstractRenderCommand):
    def __new__(cls):
        render_cmd_instance = super().__new__(cls, command_renderer)
        render_cmd_instance.visual_components = [
            '',
            VisualComponent.create('logo'),
        ]
        return render_cmd_instance


from software_release.repository_interface import RepositoryInterface


@CommandClass.register_as_subclass('render-repository')
class RenderRepository(AbstractRenderCommand):
    def __new__(cls, repository: RepositoryInterface):
        render_cmd_instance = super().__new__(cls, command_renderer)
        render_cmd_instance.visual_components = [
            '',
            VisualComponent.create('repository', repository.directory_path),
        ]
        return render_cmd_instance


@CommandClass.register_as_subclass('render-active-branch')
class RenderActiveBranch(AbstractRenderCommand):
    def __new__(cls, repository: RepositoryInterface):
        render_cmd_instance = super().__new__(cls, command_renderer)
        render_cmd_instance.visual_components = [
            '',
            VisualComponent.create('active-branch', repository.active_branch.name),
        ]
        return render_cmd_instance



@CommandClass.register_as_subclass('render-repo-info')
class RenderRepositoryInformation(AbstractRenderCommand):

    def __init__(self, repository: RepositoryInterface):
        self.commands = (
            RenderRepository(repository),
            RenderActiveBranch(repository),
        )
    
    def execute(self) -> any:
        for command in self.commands:
            command.execute()
