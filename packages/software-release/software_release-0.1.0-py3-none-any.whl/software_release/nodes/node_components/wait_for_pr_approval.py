from software_release.nodes.node import Node


@Node.register_as_subclass('wait-for-pr-approval')
class WaitPullRequestApproval(Node):

    @classmethod
    def _handle(cls, request):
        cls.echo('Waiting to detect a Merge in the Remote Repository ..')

        cls.echo('\nFor example, go to github web interface, and merge the pr,'
        'after passing the ci \'build\' and getting a code review approval')
        found = cls.run(cls.command('wait-for-pr-approval',
            request.repository.org_name,
            request.repository.name,
            request.pull_request.number
        ))
        if found:
            print('FOUND')


    def handle(self, request):
        self._handle(request)
        return super().handle(request)
