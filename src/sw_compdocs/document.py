import collections.abc
import enum
import typing


from . import container


class Block:
    def __init__(self) -> None:
        if type(self) is Block:
            raise NotImplementedError


class Heading(Block):
    def __init__(self, text: str, *, level: int = 1) -> None:
        self.text: str = text
        self.level: int = level

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.text)}, level={repr(self.level)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.text == other.text and self.level == other.level
        return super().__eq__(other)


class Paragraph(Block):
    def __init__(self, text: str) -> None:
        self.text: str = text

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
            self._l[index] = value
            return

        if isinstance(index, int):
            # type cast is safe because of overloads
            value = typing.cast(str, value)

            self._l[index] = value
            return

        typing.assert_never(index)


class TableData(container.MutableSequence[TableDataRow]):
    def __init__(
        self, head: TableDataRow, iterable: collections.abc.Iterable[TableDataRow] = ()
    ) -> None:
        self.head: typing.Final[TableDataRow] = head
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
        if len(value) != len(self.head):
            raise ValueError


class Table(Block):
    def __init__(self, data: TableData) -> None:
        self.data: TableData = data

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
    def __init__(self, text: str, *, kind: CalloutKind | None = None) -> None:
        self.text: str = text
        self.kind: CalloutKind = kind if kind is not None else CalloutKind.NOTE

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self.text)}, kind={repr(self.kind)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self.text == other.text and self.kind == other.kind
        return super().__eq__(other)


class Document(container.MutableSequence[Block]):
    def shift(self, level: int = 1) -> None:
        for blk in self:
            if isinstance(blk, Heading):
                blk.level += level
