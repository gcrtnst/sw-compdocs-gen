import collections.abc
import re


class TemplateRenderer:
    def __init__(self, mapping):
        if not isinstance(mapping, collections.abc.Mapping):
            raise TemplateMappingError(
                f"template mapping must be mapping, not '{type(mapping).__name__}'"
            )

        self._d = {}
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

    def render(self, s):
        if type(s) is not str:
            raise TypeError

        def repl(match):
            key = match["key"]
            try:
                val = self._d[key]
            except KeyError:
                raise TemplateKeyError(key)
            return val

        return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, s)


def as_mapping(v):
    if not isinstance(v, collections.abc.Mapping):
        raise TypeError

    mapping = {}
    for key, val in v.items():
        if type(key) is not str:
            raise TypeError
        if type(val) is not str:
            raise TypeError

        mapping[key] = val
    return mapping


def substitute(s, mapping):
    if type(s) is not str:
        raise TypeError
    if not isinstance(mapping, collections.abc.Mapping):
        raise TypeError

    def repl(match):
        key = match["key"]
        try:
            val = mapping[key]
        except KeyError:
            raise TemplateKeyError(key)
        if type(val) is not str:
            raise TypeError
        return val

    return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, s)


class TemplateMappingError(Exception):
    pass


class TemplateKeyError(Exception):
    def __init__(self, key):
        super().__init__(key)
        self.key = key

    def __str__(self):
        return f"missing key {repr(self.key)} in template mapping"
