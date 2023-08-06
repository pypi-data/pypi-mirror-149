from semver import VersionInfo
from typing import Optional
from .version_bump_type import BumpType


class VersionString:
    def __init__(self, string: Optional[str]) -> None:
        if string is None:
            self.string = '0.0.0'
        else:
            self.string = string

    def __str__(self) -> str:
        return str(self.string)

    def __add__(self, bump_type: Optional[BumpType]):
        if not bump_type:
            return VersionString(str(self))
        if self.string == '0.0.0':
            if bump_type == 'patch':
                return '0.0.1'
            if bump_type == 'minor':
                return '0.1.0'
            return '1.0.0'
        return VersionString(str(getattr(VersionInfo.parse(self.string),
            f'bump_{bump_type}')()))

    def __bool__(self):
        return self.string != '0.0.0'

    def __eq__(self, o: object) -> bool:
        if o is None:
            return str(self) == '0.0.0'
        return str(self) == str(o)
