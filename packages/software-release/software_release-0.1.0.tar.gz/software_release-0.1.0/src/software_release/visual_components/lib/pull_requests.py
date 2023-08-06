import os
from typing import List
import attr
from ..visual_component import VisualComponent


@attr.s
@VisualComponent.register_as_subclass('pull-requests')
class PullRequestsComponent(VisualComponent):

    ARROW = '-->'
    SPACE_1 = ' '
    S = '  '

    pull_requests = attr.ib()
    attributes = attr.ib(default=attr.Factory(lambda self: {
            'number': {
                'label': 'number',
                'max_value_len': max([len(str(x.number)) for x in self.pull_requests])
            },
            'head_branch': {
                'label': '[HEAD]',
                'max_value_len': max([len(x.head_ref) for x in self.pull_requests])
            },
            'base_branch': {
                'label': '[BASE]',
                'max_value_len': max([len(str(x.base_ref)) for x in self.pull_requests])
            },
            'state': {
                'label': '[State]',
                'max_value_len': max([len(str(x.state)) for x in self.pull_requests])
            },
            'title': {
                'label': '[Title]',
                'max_value_len': max([len(str(x.title)) for x in self.pull_requests])
            },
            'merged': {
                'label': '[Merged]',
                'extractor': lambda x: {True: 'yes', False: 'no'}[x],
                'max_value_len': 0
            },
            'arrow': {
                'label': '',
                'max_value_len': len(self.ARROW)
            },
        }, takes_self=True))

    def __attrs_post_init__(self):

        self.attributes['merged']['max_value_len'] = \
            max([len(self.attributes['merged']['extractor'](x.merged)) for x in self.pull_requests])

    def _first_line(self):
        return (
            f'{" " * len(self.SPACE_1)}'
            f'{self.attributes["number"]["label"]}{self._fl_sp("number")}'
            f'{self.attributes["head_branch"]["label"]}{self._fl_sp("head_branch")}'
            f'{self.attributes["arrow"]["label"]}{self._fl_sp("arrow")}'
            f'{self.attributes["base_branch"]["label"]}{self._fl_sp("base_branch")}'
            f'{self.attributes["state"]["label"]}{self._fl_sp("state")}'
            f'{self.attributes["merged"]["label"]}{self._fl_sp("merged")}'
            f'{self.attributes["title"]["label"]}'
        )

    def _string(self, attribute, value):
        return f"{' ' * (max(self.attributes[attribute]['max_value_len'], len(self.attributes[attribute]['label'])) - len(str(value)))}{self.S}"

    def _fl_sp(self, attribute):
        return self._string(attribute, self.attributes[attribute]['label'])

    def pr_line(self, number, head, base, state, merged, title):
        merged_value = self.attributes['merged'].get('extractor', lambda x: x)(merged)
        return f'{self.SPACE_1}' \
               f'{number}{self._string("number", number)}' \
               f'{head}{self._string("head_branch", head)}' \
               f'{self.ARROW}{self._string("arrow", self.ARROW)}' \
               f'{base}{self._string("base_branch", base)}' \
               f'{state}{self._string("state", state)}' \
               f'{merged_value}{self._string("merged", merged_value)}' \
               f'{title}'

    def render(self):
        return [
            f'\n{self._first_line()}\n',
            '\n'.join([self.pr_line(
                pr.number,
                pr.head_ref,
                pr.base_ref,
                pr.state,
                pr.merged,
                pr.title,
            ) for pr in self.pull_requests]) + '\n',
        ]
