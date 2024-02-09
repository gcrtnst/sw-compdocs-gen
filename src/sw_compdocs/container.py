import collections.abc
import typing


_T = typing.TypeVar("_T")
_T_co = typing.TypeVar("_T_co", covariant=True)


class Sequence(collections.abc.Sequence[_T_co]):
    def __init__(self, iterable: collections.abc.Iterable[_T_co] = ()) -> None:
        self._l = list(iterable)

    @typing.overload
    def __getitem__(self, index: int) -> _T_co: ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.Self: ...

    def __getitem__(self, index: int | slice) -> _T_co | typing.Self:
        if isinstance(index, int):
            return self._l[index]
        if isinstance(index, slice):  # type: ignore[misc]  # suppress warning for Any types in slice type
            return type(self)(self._l[index])
        typing.assert_never(index)

    def __len__(self) -> int:
        return len(self._l)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self._l == other._l
        return super().__eq__(other)


class MutableSequence(collections.abc.MutableSequence[_T]):
    def __init__(self, iterable: collections.abc.Iterable[_T] = ()):
        self._l: typing.List[_T] = []
        self[:] = iterable

    @typing.overload
    def __getitem__(self, index: int) -> _T: ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.Self: ...

    def __getitem__(self, index: int | slice) -> _T | typing.Self:
        if isinstance(index, int):
            return self._l[index]
        if isinstance(index, slice):  # type: ignore[misc]  # suppress warning for Any types in slice type
            return type(self)(self._l[index])
        typing.assert_never(index)

    @typing.overload
    def __setitem__(self, index: int, value: _T) -> None: ...

    @typing.overload
    def __setitem__(
        self, index: slice, value: collections.abc.Iterable[_T]
    ) -> None: ...

    def __setitem__(
        self, index: int | slice, value: _T | collections.abc.Iterable[_T]
    ) -> None:
        if isinstance(index, slice):  # type: ignore[misc]  # suppress warning for Any types in slice type
            # type cast is safe because of overloads
            value = typing.cast(collections.abc.Iterable[_T], value)

            value = self._check_value_iter(value)
            self._l[index] = value
            return
        if isinstance(index, int):
            # type cast is safe because of overloads
            value = typing.cast(_T, value)

            self._check_value(value)
            self._l[index] = value
            return
        typing.assert_never(index)

    @typing.overload
    def __delitem__(self, index: int) -> None: ...

    @typing.overload
    def __delitem__(self, index: slice) -> None: ...

    def __delitem__(self, index: int | slice) -> None:
        del self._l[index]

    def __len__(self) -> int:
        return len(self._l)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return self._l == other._l
        return super().__eq__(other)

    def insert(self, index: int, value: _T) -> None:
        self._check_value(value)
        self._l.insert(index, value)

    def _check_value_iter(
        self, value_iter: collections.abc.Iterable[_T]
    ) -> collections.abc.Iterable[_T]:
        for value in value_iter:
            self._check_value(value)
            yield value

    def _check_value(self, value: _T) -> None:
        pass
