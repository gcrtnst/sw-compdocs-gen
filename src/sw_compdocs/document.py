import collections.abc


class Document(collections.abc.MutableSequence):
    def __init__(self, iterable=()):
        self._l = []
        self[:] = iterable

    def __getitem__(self, key):
        return self._l[key]

    def __setitem__(self, key, value):
        if type(key) is slice:
            value = (v for v in value if self._check_type(v) or True)
        else:
            self._check_type(value)
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
        self._check_type(v)
        self._l.insert(i, v)

    @classmethod
    def _check_type(self, v):
        if not isinstance(v, Block):
            raise TypeError


class Block:
    def __init__(self):
        if type(self) is Block:
            raise NotImplementedError


class Heading(Block):
    __match_args__ = ("text",)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if type(value) is not str:
            raise TypeError
        self._text = value

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"{type(self).__name__}(text={repr(self.text)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self.text == other.text
        return super().__eq__(other)


class Paragraph(Block):
    __match_args__ = ("text",)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if type(value) is not str:
            raise TypeError
        self._text = value

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"{type(self).__name__}(text={repr(self.text)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self.text == other.text
        return super().__eq__(other)


class Table(Block):
    __match_args__ = ("data",)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if type(value) is not TableData:
            raise TypeError
        self._data = value

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"{type(self).__name__}(data={repr(self.data)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self.data == other.data
        return super().__eq__(other)


class TableData(collections.abc.MutableSequence):
    head = property(lambda self: self._head)

    def __init__(self, head, iterable=()):
        if type(head) is not TableDataRow:
            raise TypeError

        self._head = head
        self._l = []
        self[:] = iterable

    def __getitem__(self, key):
        return self._l[key]

    def __setitem__(self, key, value):
        if type(key) is slice:
            value = (v for v in value if self._check_item(v) or True)
        else:
            self._check_item(value)
        self._l[key] = value

    def __delitem__(self, key):
        del self._l[key]

    def __len__(self):
        return len(self._l)

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.head)}, {repr(self._l)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self.head == other.head and self._l == other._l
        return super().__eq__(other)

    def insert(self, i, v):
        self._check_item(v)
        self._l.insert(i, v)

    def _check_item(self, v):
        if type(v) is not TableDataRow:
            raise TypeError
        if len(v) != len(self.head):
            raise ValueError


class TableDataRow(collections.abc.Sequence):
    def __init__(self, iterable=()):
        l = list(iterable)
        for v in l:
            self._check_type(v)
        self._l = l

    def __getitem__(self, key):
        return self._l[key]

    def __setitem__(self, key, value):
        if type(key) is slice:
            value = list(value)
            if len(self[key]) != len(value):
                raise ValueError
            for v in value:
                self._check_type(v)
        else:
            self._check_type(value)
        self._l[key] = value

    def __len__(self):
        return len(self._l)

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other):
        if type(self) is type(other):
            return self._l == other._l
        return super().__eq__(other)

    @classmethod
    def _check_type(cls, v):
        if type(v) is not str:
            raise TypeError
