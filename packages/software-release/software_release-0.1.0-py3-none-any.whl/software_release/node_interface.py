from abc import ABC, abstractmethod


class NodeInterface(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
