import click

from .app_commands import *
from .repository_factory import RepositoryFactory
from .release_wizard import ReleaseWizard


def build_interactive_console_release_wizard(repo, main_branch='master'):
    """Build a Prototype Console Release Wizard.

    Prerequisites:
        - environment variable GH_TOKEN to authenticate with github API
        - your git HEAD should point to a 'release' branch
        - the 'release' branch should have 'tracking information' set up
        - the 'master' should be up-to-date with the remote

    Recommendations:
        - 'release' should have been branched of off 'master' to avoid conflicts on merge

    Args:
        repo ([type]): [description]
        main_branch (str, optional): [description]. Defaults to 'master'.

    Returns:
        [type]: [description]
    """
    return ReleaseWizard.create(repo, [
        'welcome-to-app',
        'sleep_0.5',

        'welcome-to-wizard-node',
        'set-release-branch_{branch}'.format(branch=main_branch),

        'active-branch-check',  # if we are NOT on a branch named 'release', exit
        'sleep_0.35',

        'determine-new-version',
        # 'pull-branch-with-releases',  # ie pull master branch
        'sleep_0.35',

        'version-bump',
        'sleep_0.35',

        'branch-references',
        'changelog',
        'sleep_0.35',

        'push-active-branch',

        'sleep_0.35',
        'open-pull-request',

        'sleep_0.35',
        'get-pull-requests',

        'wait-for-pr-approval',

        # TODO attempt to push from local master to remote master in case the
        # merge happened locally first (and then pushed) in contrast to doing
        # the merge on github (online) through the github web interface

        'pull-branch-with-releases',  # pull master branch

        'tag-commit-on-branch-with-releases',
        'push-tag',
    ])



def build_changelog_diff_wizard(repo, main_branch='master'):
    return ReleaseWizard.create(repo, [
        'set-release-branch_{branch}'.format(branch=main_branch),

        'determine-new-version',
        # 'pull-branch-with-releases',  # ie pull master branch
        # 'sleep_0.35',

        # 'changelog',
    ])

@click.option('--path', '-p', 'repo_path', default='.', type=str, show_default=True)
@click.command()
# @click.option('--changelog', '-cl', 'changelog', type=bool, default=False)
@click.option('--changelog', '-cl', default=False, is_flag=True, show_default=True,
    help="Just show the computed Changelog Diff")

def cli(repo_path: str, changelog: bool):
    
    repo = RepositoryFactory.create(repo_path)

    if changelog:  # show the automatically generated changelog addition (diff)
        # c = build_changelog_diff_wizard
        pass
    else:
        c = build_interactive_console_release_wizard
    
    release_wizard = c(repo)
    
    release_wizard.run()
