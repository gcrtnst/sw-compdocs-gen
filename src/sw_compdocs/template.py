import collections.abc
import re
import typing


class TemplateKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key: typing.Final[str] = key

    def __str__(self) -> str:
        return f"missing replacement string for placeholder $[{self.key}]"


class TemplateFormatter:
    def __init__(self, mapping: collections.abc.Mapping[str, str]) -> None:
        self._d: dict[str, str] = dict(mapping)

    def format(self, s: str) -> str:
        def repl(match: re.Match[str]) -> str:
            key: str = match["key"]
            try:
                val = self._d[key]
            except KeyError as exc:
                raise TemplateKeyError(key) from exc
            return val

        return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, s)
