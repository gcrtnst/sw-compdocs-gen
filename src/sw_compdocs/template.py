import re


def as_str(v):
    if not isinstance(v, str):
        raise TypeError
    return str(v)


def as_mapping(v):
    mapping = {}
    for key, val in v.items():
        key = as_str(key)
        val = as_str(val)

        if re.search("\A[A-Za-z0-9_]+\Z", key) is None:
            raise ValueError

        mapping[key] = val
    return mapping


def substitute(s, mapping):
    s = as_str(s)
    mapping = as_mapping(mapping)

    def repl(match):
        key = match["key"]
        try:
            return mapping[key]
        except KeyError:
            raise TemplateKeyError(key)

    return re.sub(r"(?s:\$\[(?P<key>.*?)\])", repl, s)


class TemplateKeyError(KeyError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key
