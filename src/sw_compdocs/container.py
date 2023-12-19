import collections.abc


class Sequence(collections.abc.Sequence):
    def __init__(self, iterable=()):
        self._l = list(iterable)

    def __getitem__(self, key):
        return self._l[key]

    def __len__(self):
        return len(self._l)

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self._l == other._l
        return super().__eq__(other)


class MutableSequence(collections.abc.MutableSequence):
    def __init__(self, iterable=()):
        self._l = []
        self[:] = iterable

    def __getitem__(self, key):
        return self._l[key]

    def __setitem__(self, key, value):
        if type(key) is slice:
            value = (v for v in value if self._check_value(v) or True)
        else:
            self._check_value(value)
        self._l[key] = value

    def __delitem__(self, key):
        del self._l[key]

    def __len__(self):
        return len(self._l)

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self._l == other._l
        return super().__eq__(other)

    def insert(self, i, v):
        self._check_value(v)
        self._l.insert(i, v)

    def _check_value(self, value):
        pass
