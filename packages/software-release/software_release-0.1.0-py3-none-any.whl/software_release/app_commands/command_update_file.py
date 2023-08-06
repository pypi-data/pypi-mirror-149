import os
import json

from software_release.commands.command_class import CommandClass
from software_release.repository_interface import RepositoryInterface


from software_release.commands.base_command import BaseCommand
import re
from typing import Tuple

import logging


logger = logging.getLogger(__name__)

RegExPair = Tuple[str, str]

RegExPairs = Tuple[RegExPair]

FileRegexes = Tuple[RegExPairs]


__all__ = ['UpdateVersionStringCommand', 'UpdateBranchReferencesCommand',
    'UpdateChangelogCommand']


SEMVER_REGEX = r'\d+\.\d+\.\d+'


class AbstractUpdateFilesCommand(BaseCommand):

    def __new__(cls, files: Tuple[str], regexes: FileRegexes):
        return super().__new__(cls, re, 'sub', files, regexes)

    def execute(self):
        return list(filter(None, [self.update_file(file_path, regex_pairs)
            for file_path, regex_pairs in zip(self.args[0], self.args[1])]))

    def update_file(self, file_path: str, regex_pairs: RegExPairs):
        with open(file_path, mode='r') as fr:
            initial_content = fr.read()

        content = str(initial_content)
        for match_regex, replace_regex in regex_pairs:
            content = re.sub(match_regex, replace_regex, content)

        file_content_changed = content != initial_content

        if file_content_changed:
            with open(file_path, mode='w') as fw:
                fw.write(content)
            return file_path

    @classmethod
    def file_path(cls, repository_root_path):
        def _file_path(*paths):
            return os.path.join(repository_root_path, *paths)
        return _file_path


from software_release.config_reader import config


@CommandClass.register_as_subclass('update-version-string')
class UpdateVersionStringCommand(AbstractUpdateFilesCommand):

    def __new__(cls, repository: RepositoryInterface, current_version, new_version: str):
        file_path = cls.file_path(repository.directory_path)
        repo_config = config(repository.directory_path)
        
        files = [
            file_path('setup.cfg'),
            file_path('README.rst'),
        ]
        regexes = [
            # setup.cfg
            (
                (
                    fr'(version\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
                (
                    r'(download_url\s*=\s*https://github.com/{username}/{repo}/archive/v){prev_version}(.tar.gz)'.format(
                        username=repository.org_name, repo=repository.name, prev_version=current_version),
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
            # README.rst
            (
                (
                    fr'(["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ),
        ]
        # optional python file; ie package_name/sre/__init__.py
        if 'version_variable' in repo_config['semantic_release']:
            version_file_path, version_variable_name = repo_config['semantic_release']['version_variable'].split(':')
            files.append(file_path(*list(version_file_path.split('/'))))
            regexes.append((
                (
                    fr'({version_variable_name}\s*=\s*["\']?v?){current_version}(["\']?)',
                    fr"\g<1>{new_version}\g<2>"
                ),
            ))
        else:
            # TODO change raised Exception to something more specific
            raise RuntimeError("Section [semantic_release] not found in Repo "
                "Config (ie setup.cfg)")
        cmd_instance = super().__new__(cls, files, regexes)
        return cmd_instance


@CommandClass.register_as_subclass('update-branch-refs')
class UpdateBranchReferencesCommand(AbstractUpdateFilesCommand):

    def __new__(cls, repository: RepositoryInterface, branch_name):
        file_path = cls.file_path(repository.directory_path)
        
        files = [
            file_path('README.rst'),
        ]
        regexes = [
            # README.rst
            (
                (
                    fr'(compare/v{SEMVER_REGEX}\.\.\.?)([\w\-_\d]+)',
                    fr"\g<1>{branch_name}"
                ),
            ),
        ]

        cmd_instance = super().__new__(cls, files, regexes)
        return cmd_instance



from software_release.angular_parser import parse_commit_message, \
    UnknownCommitMessageStyleError
from software_release.commit_generator import BranchCommitsGenerator
re_breaking = re.compile('BREAKING CHANGE: (.*)')


def my_get_changelog(commit_generator) -> dict:
    """
    Generates a changelog from given version till HEAD.\n
    :param from_version: The last version not in the changelog. The changelog
                         will be generated from the commit after this one.
    :return: a dict with different changelog sections
    """
    changes: dict = {
        'feature': [],
        'fix': [],
        'test': [],
        'documentation': [],
        'refactor': [],
        'breaking': [],
        'performance': [],
        'improvement': [],
        'ci': []
    }

    for commit in iter(commit_generator):
        commit_message = commit.message
        _hash = commit.sha

        try:
            # [level_bump [3,2,1], type [feature, fix, etc], 'scope', 'subject']
            message = parse_commit_message(commit_message)
            if message[1] not in changes:
                continue

            changes[message[1]].append((_hash, message[3][0]))

            if len(message[3]) > 1:
                if 'BREAKING CHANGE' in message[3][1]:
                    parts = re_breaking.match(message[3][1])
                    if parts:
                        changes['breaking'].append((_hash, parts.group(1)))
                if len(message[3]) > 2:
                    if message[3][2] and 'BREAKING CHANGE' in message[3][2]:
                        parts = re_breaking.match(message[3][2])
                        if parts:
                            changes['breaking'].append((_hash, parts.group(1)))

        except UnknownCommitMessageStyleError as err:
            pass

    return changes


CHANGELOG_SECTIONS = [
    'feature',
    'fix',
    'test',
    'breaking',
    'documentation',
    'performance',
    'ci',
]

def rst_changelog(new_version: str, changelog: dict, date: str = None, header: bool = False) -> str:
    """
    Generates an rst version of the changelog. It preserves sections\n
    - 'feature'
    - 'fix'
    - 'breaking'
    - 'documentation'
    - 'performance'

    :param str new_version: A string with the version number.
    :param dict changelog: A dict holding the items per section from generate_changelog.
    :param bool header: A boolean that decides whether a changes subsection should be included or not.
    :param str date: an optional date to include in subsection generated along with the version
    :return: The rst formatted changelog.
    """
    if new_version[0] == 'v':
        new_version = new_version[1:]
    b = new_version
    if date:
        b += ' ({})'.format(date)
    b += '\n{}'.format('-' * len(b))

    s = '^'
    if header:
        header_string = 'Changes'
        b += '\n\n{}\n{}'.format(header_string, len(header_string)*s)
        s = '"'
    b += '\n\n' + '\n\n'.join([get_change_type(changelog, section, s) for section in CHANGELOG_SECTIONS if changelog[section]])
    return b.strip()


def get_change_type(changelog: dict, section: str, symbol: str) -> str:
    return '{}\n{}\n{}'.format(section, len(section)*symbol, '\n'.join('- {}'.format(commit_message) for commit_hash, commit_message in changelog[section]))


@CommandClass.register_as_subclass('update-changelog')
class UpdateChangelogCommand(AbstractUpdateFilesCommand):
    # TODO: examining the automatically generated changelog file we see commit from 
    # previous release already on master branch
    # 
    # FIX: generate the correct commits Head --> Tag-on-master
    
    def __new__(cls, repository: RepositoryInterface, current_version, new_version, date):
        if bool(current_version):
            current_version = f'v{current_version}'
        file_path = cls.file_path(repository.directory_path)
        default_changelog_file = 'CHANGELOG.rst'
        SECTION = 'Changelog'
        SECTION_DIRECTIVE = '=' * len(SECTION)
        changelog_dict = my_get_changelog(BranchCommitsGenerator(repository, current_version))
        changelog_rst_string = rst_changelog(str(new_version), changelog_dict, date)

        if not changelog_rst_string:
            logger.error("No Changelog Content Generated: %s", json.dumps({
                'changelog_item_types': '[' + ', '.join([str(x) for x in changelog_dict.keys()]) + ']',
                'changelog_rst_string': changelog_rst_string,
            }))

        files = [
            file_path(default_changelog_file),
        ]
        regexes = [
            # CHANGELOG.rst
            (
                (
                    fr'({SECTION}\n{SECTION_DIRECTIVE}\n+)(v?{current_version})',
                    fr'\g<1>{changelog_rst_string}\n\n\n\g<2>'
                ),
            ),
        ]

        cmd_instance = super().__new__(cls, files, regexes)
        cmd_instance.changes_added = changelog_rst_string
        return cmd_instance

    def execute(self) -> None:
        files_changed = super().execute()
        if not files_changed:
            res = None
        else:
            res = files_changed[0]
        return files_changed, self.changes_added
