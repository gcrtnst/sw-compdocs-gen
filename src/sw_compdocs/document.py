import collections.abc
import enum
import typing


from . import container


class Block:
    def __init__(self) -> None:
        if type(self) is Block:
            raise NotImplementedError


class Heading(Block):
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._text = value

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        if type(value) is not int:
            raise TypeError
        if value < 1 or 6 < value:
            raise ValueError
        self._level = value

    def __init__(self, text: str, *, level: int = 1) -> None:
        self.text = text
        self.level = level

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.text)}, level={repr(self.level)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.text == other.text and self.level == other.level
        return super().__eq__(other)


class Paragraph(Block):
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._text = value

    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.text)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.text == other.text
        return super().__eq__(other)


class TableDataRow(container.Sequence[str]):
    def __init__(self, iterable: collections.abc.Iterable[str] = ()) -> None:
        super().__init__(iterable)

        if len(self) <= 0:
            raise ValueError
        for v in self:
            self._check_type(v)

    @typing.overload
    def __setitem__(self, index: int, value: str) -> None:
        ...

    @typing.overload
    def __setitem__(self, index: slice, value: collections.abc.Iterable[str]) -> None:
        ...

    def __setitem__(
        self, index: int | slice, value: str | collections.abc.Iterable[str]
    ) -> None:
        if isinstance(index, slice):  # type: ignore[misc]  # suppress warning for Any types in slice type
            # type cast is safe because of overloads
            value = typing.cast(collections.abc.Iterable[str], value)

            value = list(value)
            if len(self[index]) != len(value):
                raise ValueError
            for v in value:
                self._check_type(v)
            self._l[index] = value
            return

        if isinstance(index, int):
            # type cast is safe because of overloads
            value = typing.cast(str, value)

            self._check_type(value)
            self._l[index] = value
            return

        typing.assert_never(index)

    @classmethod
    def _check_type(cls, v: str) -> None:
        if type(v) is not str:
            raise TypeError


class TableData(container.MutableSequence[TableDataRow]):
    @property
    def head(self) -> TableDataRow:
        return self._head

    def __init__(
        self, head: TableDataRow, iterable: collections.abc.Iterable[TableDataRow] = ()
    ) -> None:
        if type(head) is not TableDataRow:
            raise TypeError
        self._head = head

        super().__init__(iterable)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.head)}, {repr(self._l)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            if self.head != other.head:
                return False
        return super().__eq__(other)

    def _check_value(self, value: TableDataRow) -> None:
        if type(value) is not TableDataRow:
            raise TypeError
        if len(value) != len(self.head):
            raise ValueError


class Table(Block):
    @property
    def data(self) -> TableData:
        return self._data

    @data.setter
    def data(self, value: TableData) -> None:
        if type(value) is not TableData:
            raise TypeError
        self._data = value

    def __init__(self, data: TableData) -> None:
        self.data = data

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.data)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.data == other.data
        return super().__eq__(other)


@enum.unique
class CalloutKind(enum.Enum):
    NOTE = enum.auto()
    WARNING = enum.auto()


class Callout(Block):
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._text = value

    @property
    def kind(self) -> CalloutKind:
        return self._kind

    @kind.setter
    def kind(self, value: CalloutKind) -> None:
        if type(value) is not CalloutKind:
            raise TypeError
        self._kind = value

    def __init__(self, text: str, *, kind: CalloutKind | None = None) -> None:
        self.text = text
        self.kind = kind if kind is not None else CalloutKind.NOTE

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.text)}, kind={repr(self.kind)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.text == other.text and self.kind == other.kind
        return super().__eq__(other)


class Document(container.MutableSequence[Block]):
    def _check_value(self, value: Block) -> None:
        if not isinstance(value, Block):
            raise TypeError

    def shift(self, level: int = 1) -> None:
        if type(level) is not int:
            raise TypeError

        for blk in self:
            if isinstance(blk, Heading):
                blk.level += level
