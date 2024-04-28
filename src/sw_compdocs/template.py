import collections.abc
import re
import typing


class TemplateKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key: typing.Final[str] = key

    def __str__(self) -> str:
        return f"missing replacement string for placeholder $[{self.key}]"


def format(template: str, mapping: collections.abc.Mapping[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        key: str = match["key"]
        try:
            val = mapping[key]
        except KeyError as exc:
            raise TemplateKeyError(key) from exc
        return val

    return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, template)
