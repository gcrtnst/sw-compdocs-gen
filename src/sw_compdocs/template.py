import collections.abc
import re

from . import convert as dot_convert


def as_mapping(v):
    if not isinstance(v, collections.abc.Mapping):
        raise TypeError

    mapping = {}
    for key, val in v.items():
        key = dot_convert.as_str(key)
        val = dot_convert.as_str(val)

        if re.search("\A[A-Za-z0-9_]+\Z", key) is None:
            raise ValueError

        mapping[key] = val
    return mapping


def substitute(s, mapping):
    s = dot_convert.as_str(s)
    if not isinstance(mapping, collections.abc.Mapping):
        raise TypeError

    def repl(match):
        key = match["key"]
        try:
            val = mapping[key]
        except KeyError:
            raise TemplateKeyError(key)
        return dot_convert.as_str(val)

    return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, s)


class TemplateKeyError(KeyError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key
