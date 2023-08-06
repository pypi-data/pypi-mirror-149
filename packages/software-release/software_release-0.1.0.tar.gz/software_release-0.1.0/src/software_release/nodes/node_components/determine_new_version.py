from typing import Union
from software_release.nodes.node import Node
from software_release.version_class import VersionString


@Node.register_as_subclass('determine-new-version')
class DetermineNewVersionNode(Node):

    @classmethod
    def _handle(cls, request):
        
        # TODO isolate finding of previous version in its own Node
        # Simple detection of release by looking at git tags on master branch
        # stripped of 'v'
        previous_version: Union[None, str] = cls.run(cls.command('previous-release', request.repository))

        # If no previous release found, show a message
        if previous_version is None:
            cls.run(cls.command('render', 'no-release-tag-found'))
            cls.run(cls.command('render',
                f'\nIt seems this is the first ever semantic release we are about to make!\n',
                ' We shall assume that the previously released was made under'
                'the imaginary tag v0.0.0 for the purpose of automatically'
                'recommending the next release version.\n',
            ))
        else:  # previous release found, show a message
            cls.run(cls.command('render', 'release-tag-found', previous_version))

        # inform about how the next version estimation is computed
        cls.run(cls.command('render',
            "We examine the commits found in revision 'HEAD..master' and try to parse their "
            "messages, using the Angular Parser, in order to make an estimation of what kind "
            "of changes (ie new feature, bug fixes, ci changes, documnetation changes) are "
            "introduced from the commits in the new release\n",
            "Based on the discovered changes we estimate a 'version bump'.\n",
            " Then :: 'previous_release' + 'version_bump' = 'next_release'\n"
        ))

        # Automatically recommend next semantic version
        # TODO fixate interface so it returns the same type and avoid doing if-else here!
        result = cls.run(cls.command('new-release',
            request.repository, VersionString(previous_version), force_version=None))
        new_version: VersionString = result[0]
        level_bump: Union[None, str] = result[1]

        if not level_bump:
            # proposed_new_version = str(result)
            minimum_release = new_version + 'patch'
            pre_release_delimeter = '-'
            recommend = [
                '{version}{sep}{pre_release_tag}'.format(
                    version=minimum_release,
                    sep=pre_release_delimeter,
                    pre_release_tag='dev'
                ),
                '{version}'.format(
                    version=minimum_release
                ),
                '{version}{sep}{pre_release_tag}'.format(
                    version=minimum_release,
                    sep=pre_release_delimeter,
                    pre_release_tag='pre'
                ),
            ]
        else:  # version bump is at least PATCH!
            recommend = [str(new_version)]

        cls.run(cls.command('render',
            f' Production Release with version bump: {level_bump}\n',
            f' --> {previous_version} + {level_bump} bump = {new_version}'
        ))

        dialog = cls.dialog('recommended-or-override-version')
        input_new_version = dialog.dialog({
            'quick-recommendations': recommend,
        })
        import re
        build_version = r'[a-zA-Z]+(?:\.\d+)?'
        regex = fr'v?(\d+\.\d+\.\d+(?:[\.\-_]?{build_version}(?:\.{build_version})*)?)'

        cmd_1 = cls.command('render', 'Incorrect input version.\n',
                'Please make sure your input is a valid Semantic Version;\n',
                'MAJOR.MINOR.PATCH',
                f'Should match regex: {regex}'
            )
        match = re.match(regex, input_new_version)
        while not match:
            cls.run(cmd_1)
            input_new_version = dialog.dialog({
                'quick-recommendations': recommend,
            })
            match = re.match(regex, input_new_version)

        new_version = match.group(1)

        command = cls.command('render', 'new-release-version', new_version)
        cls.run(command)
        return previous_version, new_version

    def handle(self, request):
        previous_version, new_version = self._handle(request)
        request.previous_version = previous_version
        request.new_version = new_version
        return super().handle(request)
