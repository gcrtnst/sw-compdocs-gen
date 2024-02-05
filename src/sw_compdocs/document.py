import collections.abc
import dataclasses
import enum
import typing


from . import container


class Block:
    def __init__(self) -> None:
        if type(self) is Block:
            raise NotImplementedError


@dataclasses.dataclass
class Heading(Block):
    text: str
    _: dataclasses.KW_ONLY
    level: int = 1


@dataclasses.dataclass
class Paragraph(Block):
    text: str


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


@dataclasses.dataclass
class Table(Block):
    data: TableData


@enum.unique
class CalloutKind(enum.Enum):
    NOTE = enum.auto()
    WARNING = enum.auto()


@dataclasses.dataclass
class Callout(Block):
    text: str
    _: dataclasses.KW_ONLY
    kind: CalloutKind = CalloutKind.NOTE


class Document(container.MutableSequence[Block]):
    def shift(self, level: int = 1) -> None:
        for blk in self:
            if isinstance(blk, Heading):
                blk.level += level
