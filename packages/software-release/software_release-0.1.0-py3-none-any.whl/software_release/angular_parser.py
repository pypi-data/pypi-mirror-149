"""
Angular commit style parser

https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines
"""
import logging
import re
from typing import List
from collections import namedtuple

logger = logging.getLogger(__name__)


re_breaking = re.compile("BREAKING[ -]CHANGE: (.*)")


ParsedCommit = namedtuple(
    "ParsedCommit", ["bump", "type", "scope", "descriptions"]
)


def parse_paragraphs(text: str) -> List[str]:
    """
    This will take a text block and return a tuple containing each
    paragraph with single line breaks collapsed into spaces.

    :param text: The text string to be divided.
    :return: A tuple of paragraphs.
    """
    return [
        paragraph.replace("\n", " ")
        for paragraph in text.split("\n\n")
        if len(paragraph) > 0
    ]




# Supported commit types for parsing
TYPES = {
    'feat': 'feature',
    'fix': 'fix',
    'test': 'test',
    'docs': 'documentation',
    'style': 'style',
    'refactor': 'refactor',
    'build': 'build',
    'ci': 'ci',
    'perf': 'performance',
    'chore': 'chore',
    'revert': 'revert',
    'improvement': 'improvement'
}

re_parser = re.compile(
    r"(?P<type>" + "|".join(TYPES.keys()) + ")"
    r"(?:\((?P<scope>[^\n]+)\))?"
    r"(?P<break>!)?: "
    r"(?P<subject>[^\n]+)"
    r"(:?\n\n(?P<text>.+))?",
    re.DOTALL,
)

MINOR_TYPES = [
    "feat",
]

PATCH_TYPES = [
    "fix",
    "perf",
]


def parse_commit_message(message: str) -> ParsedCommit:
    """
    Parse a commit message according to the angular commit guidelines specification.

    :param message: A string of a commit message.
    :return: A tuple of (level to bump, type of change, scope of change, a tuple with descriptions)
    :raises UnknownCommitMessageStyleError: if regular expression matching fails
    """
    # Attempt to parse the commit message with a regular expression
    parsed = re_parser.match(message)
    if not parsed:
        raise UnknownCommitMessageStyleError(
            "Unable to parse the given commit message: {}".format(message)
        )

    if parsed.group("text"):
        descriptions = parse_paragraphs(parsed.group("text"))
    else:
        descriptions = list()
    # Insert the subject before the other paragraphs
    descriptions.insert(0, parsed.group("subject"))

    # Check for mention of breaking changes
    level_bump = 0
    if parsed.group("break") or any([re_breaking.match(p) for p in descriptions]):
        level_bump = 3  # Major

    # Set the bump level based on commit type
    if parsed.group("type") in MINOR_TYPES:
        level_bump = max([level_bump, 2])

    if parsed.group("type") in PATCH_TYPES:
        level_bump = max([level_bump, 1])

    return ParsedCommit(
        level_bump, TYPES[parsed.group("type")], parsed.group("scope"), descriptions,
    )


class UnknownCommitMessageStyleError(Exception): pass
