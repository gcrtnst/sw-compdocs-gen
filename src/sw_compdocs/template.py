import collections.abc
import re
import typing


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


class TemplateMappingError(Exception):
    pass


class TemplateKeyError(Exception):
    def __init__(self, key: object) -> None:
        super().__init__(key)
        self.key: typing.Final[object] = key

    def __str__(self) -> str:
        return f"missing key {repr(self.key)} in template mapping"
