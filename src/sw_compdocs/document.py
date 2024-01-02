from . import container


class Document(container.MutableSequence):
    def _check_value(self, value):
        if not isinstance(value, Block):
            raise TypeError


class Block:
    def __init__(self):
        if type(self) is Block:
            raise NotImplementedError


class Heading(Block):
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


class TableData(container.MutableSequence):
    head = property(lambda self: self._head)

    def __init__(self, head, iterable=()):
        if type(head) is not TableDataRow:
            raise TypeError
        self._head = head

        super().__init__(iterable)

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.head)}, {repr(self._l)})"

    def __eq__(self, other):
        if type(self) is type(other) and self.head != other.head:
            return False
        return super().__eq__(other)

    def _check_value(self, value):
        if type(value) is not TableDataRow:
            raise TypeError
        if len(value) != len(self.head):
            raise ValueError


class TableDataRow(container.Sequence):
    def __init__(self, iterable=()):
        super().__init__(iterable)

        if len(self) <= 0:
            raise ValueError
        for v in self:
            self._check_type(v)

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

    @classmethod
    def _check_type(cls, v):
        if type(v) is not str:
            raise TypeError
