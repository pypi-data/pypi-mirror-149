from .git_status import GitStatus


class GitStatusFactory:

    @staticmethod
    def create(repository) -> GitStatus:
        return GitStatus.from_repo(repository)
