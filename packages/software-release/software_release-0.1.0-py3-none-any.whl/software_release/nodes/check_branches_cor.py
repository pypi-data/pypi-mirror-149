from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional

from ..branch_checker import BranchChecker


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)
        return request



import attr

@attr.s
class ActiveBranchHandler(AbstractHandler):
    """Check if active branch is a proper 'release' branch.
    
    If the check is successful, passes the request to the next handler.
    If not, the request is not processed further.
    """
    branch_checker = attr.ib(init=False, default=attr.Factory(BranchChecker))

    def handle(self, request: Any) -> str:
        active_branch = self.branch_checker.active_branch(request.repository)
        if self.branch_checker.is_release_branch(active_branch):
            return super().handle(request)


def _create_chain():
    check_active_branch = ActiveBranchHandler()


@attr.s
class CheckBranchesCoR:
    handlers = attr.ib(default=_create_chain)

    def handle(self, request):
        return self.handlers.handle(request)
