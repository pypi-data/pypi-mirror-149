from typing import Iterable

import attr

from software_release.nodes import Node
from software_release.handler import HandlerChain


@attr.s
class ReleaseWizard:
    repository = attr.ib()
    handler = attr.ib()

    @staticmethod
    def create(repository, nodes: Iterable[str]):
        node_objects = [Node.create(*node.split('_')) for node in nodes]
        return ReleaseWizard(
            repository,
            HandlerChain.from_handlers(node_objects)
        )

    def run(self):
        self.handler.handle(type('Request', (), {
            'repository': self.repository
        })())
