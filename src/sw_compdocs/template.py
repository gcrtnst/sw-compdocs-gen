import collections.abc
import re


class TemplateFormatter:
    def __init__(self, mapping: collections.abc.Mapping[str, str]) -> None:
        if not isinstance(mapping, collections.abc.Mapping):
            raise TemplateMappingError(
                f"template mapping must be mapping, not '{type(mapping).__name__}'"
            )

        self._d: dict[str, str] = {}
        for key, val in mapping.items():
            if type(key) is not str:
                raise TemplateMappingError(
                    f"template mapping entry key must be str, not '{type(key).__name__}'"
                )
            if type(val) is not str:
                raise TemplateMappingError(
                    f"template mapping entry value must be str, not '{type(val).__name__}'"
                )
            self._d[key] = val

    def format(self, s: str) -> str:
        if type(s) is not str:
            raise TypeError

        def repl(match: re.Match[str]) -> str:
            key = match["key"]
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
        self.key = key

    def __str__(self) -> str:
        return f"missing key {repr(self.key)} in template mapping"
