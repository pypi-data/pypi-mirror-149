from abc import ABC
from typing import Optional

from software_release.repository_interface import RepositoryInterface


class PushActiveBranchInterface(ABC):

    def push(self, repository: RepositoryInterface,
            remote_server_slug: Optional[str] = 'origin') -> None:
        raise NotImplementedError
