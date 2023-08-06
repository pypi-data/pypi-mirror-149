import pytest


@pytest.fixture
def build_pull_request_title_command():
    from software_release.nodes.node_components.open_pull_request import OpenPullRequestNode
    import software_release.app_commands.command_get_pr_title
    def build_pull_request_title(request):
        return OpenPullRequestNode.run(OpenPullRequestNode.command('build-pr-title', request))
    return build_pull_request_title


def test_get_pull_request_title_command(build_pull_request_title_command):
    result = build_pull_request_title_command(type('Request', (), {
        'pull_request_title': 'Test Suite Pull Request Title',
    }))
    assert result == 'Test Suite Pull Request Title'


def test_infer_pull_request_title(build_pull_request_title_command):
    result = build_pull_request_title_command(type('Request', (), {
        'repository': type('Repository', (), {'name': 'Test Suite Pull Request Title'}),
        'new_version': '0.0.2',
    }))
    assert result == 'Test Suite Pull Request Title v0.0.2 Release'
