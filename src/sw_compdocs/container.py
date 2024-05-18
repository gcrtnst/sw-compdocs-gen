import collections.abc
import typing


class Sequence[T](collections.abc.Sequence[T]):
    def __init__(self, iterable: collections.abc.Iterable[T] = ()) -> None:
        super().__init__()
        self._l = list(iterable)

    @typing.overload
    def __getitem__(self, index: int) -> T: ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.Self: ...

    def __getitem__(self, index: int | slice) -> T | typing.Self:
        if isinstance(index, slice):
            return type(self)(self._l[index])
        return self._l[index]

    def __len__(self) -> int:
        return len(self._l)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({repr(self._l)})"

    def __eq__(self, other: object) -> bool:
        if type(other) is type(self):
            return self._l == other._l
        return super().__eq__(other)


class MutableSequence[T](collections.abc.MutableSequence[T]):
    def __init__(self, iterable: collections.abc.Iterable[T] = ()) -> None:
        super().__init__()
        self._l: list[T] = []
        self[:] = iterable

    @typing.overload
    def __getitem__(self, index: int) -> T: ...

    @typing.overload
    def __getitem__(self, index: slice) -> typing.Self: ...

    def __getitem__(self, index: int | slice) -> T | typing.Self:
        if isinstance(index, slice):
            return type(self)(self._l[index])
        return self._l[index]

    @typing.overload
    def __setitem__(self, index: int, value: T) -> None: ...

    @typing.overload
    def __setitem__(self, index: slice, value: collections.abc.Iterable[T]) -> None: ...

    def __setitem__(
        self, index: int | slice, value: T | collections.abc.Iterable[T]
    ) -> None:
        if isinstance(index, slice):
            # type cast is safe because of overloads
            value = typing.cast(collections.abc.Iterable[T], value)

            value = self._check_value_iter(value)
            self._l[index] = value
        else:
            # type cast is safe because of overloads
            value = typing.cast(T, value)

            self._check_value(value)
            self._l[index] = value

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
        if type(other) is type(self):
            return self._l == other._l
        return super().__eq__(other)

    def insert(self, index: int, value: T) -> None:
        self._check_value(value)
        self._l.insert(index, value)

    def _check_value_iter(
        self, value_iter: collections.abc.Iterable[T]
    ) -> collections.abc.Iterable[T]:
        for value in value_iter:
            self._check_value(value)
            yield value

    def _check_value(self, value: T) -> None:
        pass
