from software_release.push_active_branch_interface import PushActiveBranchInterface


class ActiveBranchPusher(PushActiveBranchInterface):

    def push(self, repository, remote_server_slug='origin'):
        # try:
        # TODO: use the git API to implement t he push method
        # https://towardsdatascience.com/all-the-things-you-can-do-with-github-api-and-python-f01790fca131
        origin = repository.repo_proxy.remote(name=remote_server_slug)
        # print('\nDIR REMOTE\n', dir(origin), '\n----')
        # print('\nURLS\n', [_ for _ in origin.urls], '\n----')

        origin.push()
        self.remote_slug = remote_server_slug
        self.urls = [_ for _ in origin.urls]
        # except Exception as error:
        #     raise GitPushError(f'Push to remote \'{remote_server_slug}\' error') from error

    # def push(self, repository, remote_server_slug='origin'):
    #     import os
    #     import subprocess

    #     current_working_dir = os.getcwd()
    #     os.chdir(repository.directory_path)
        
    #     cmd_args = ['git', 'push']
    #     child_process = subprocess.run(cmd_args, capture_output=True, check=False)
    #     os.chdir(current_working_dir)
    #     self.remote_slug = remote_server_slug

    #     if child_process.returncode != 0:
    #         raise GitPushError(f"Command '{' '.join(cmd_args)}' exited with non-zero status. "
    #                        f"Stderr: {child_process.stderr.decode().strip()}")
        


class GitPushError(Exception): pass
