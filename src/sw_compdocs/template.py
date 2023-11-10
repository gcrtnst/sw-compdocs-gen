import collections.abc
import re


def as_mapping(v):
    if not isinstance(v, collections.abc.Mapping):
        raise TypeError

    mapping = {}
    for key, val in v.items():
        if type(key) is not str:
            raise TypeError
        if type(val) is not str:
            raise TypeError

        if re.search("\A[A-Za-z0-9_]+\Z", key) is None:
            raise ValueError

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


class TemplateKeyError(Exception):
    def __init__(self, key):
        super().__init__(key)
        self.key = key

    def __str__(self):
        return f"missing key {repr(self.key)} in template mapping"
