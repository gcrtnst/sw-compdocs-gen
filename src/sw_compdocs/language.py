import collections.abc
import csv
import io
import os
import typing

from . import _types
from . import container
from . import validator


class Translation:
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._id = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._description = value

    @property
    def en(self) -> str:
        return self._en

    @en.setter
    def en(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._en = value

    @property
    def local(self) -> str:
        return self._local

    @local.setter
    def local(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._local = value

    def __init__(self, id: str, description: str, en: str, local: str) -> None:
        self.id = id
        self.description = description
        self.en = en
        self.local = local

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.id!r}, {self.description!r}, {self.en!r}, {self.local!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            # type narrowing assertion for mypy 1.8.0
            assert isinstance(other, type(self))

            return (
                self.id == other.id
                and self.description == other.description
                and self.en == other.en
                and self.local == other.local
            )
        return super().__eq__(other)


class LanguageTSVDialect(csv.Dialect):
    delimiter = "\t"
    doublequote = False
    escapechar = None
    lineterminator = "\n"
    quoting = csv.QUOTE_NONE
    skipinitialspace = False
    strict = True


class LanguageTSVError(Exception):
    @property
    def msg(self) -> str:
        return self._msg

    @property
    def file(self) -> _types.StrOrBytesPath | None:
        return self._file

    @file.setter
    def file(self, value: _types.StrOrBytesPath | None) -> None:
        if value is not None and not validator.is_pathlike(value):
            raise TypeError
        self._file = value

    @property
    def line(self) -> int | None:
        return self._line

    @line.setter
    def line(self, value: int | None) -> None:
        if value is not None and type(value) is not int:
            raise TypeError
        self._line = value

    def __init__(self, msg: str) -> None:
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg
        self._file = None
        self._line = None

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else "<language.tsv>"
        line = str(self.line) if self.line is not None else "?"
        return f"{file}: line {line}: {self.msg}"


class LanguageFindError(Exception):
    pass


class LanguageFindIDError(LanguageFindError):
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._id = value

    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.id = id

    def __str__(self) -> str:
        return f"missing translation for id {self.id!r}"


class LanguageFindEnError(LanguageFindError):
    @property
    def en(self) -> str:
        return self._en

    @en.setter
    def en(self, value: str) -> None:
        if type(value) is not str:
            raise TypeError
        self._en = value

    def __init__(self, en: str) -> None:
        super().__init__(en)
        self.en = en

    def __str__(self) -> str:
        return f"missing translation for text {self.en!r}"


class Language(container.Sequence[Translation]):
    def __init__(self, iterable: collections.abc.Iterable[Translation] = ()) -> None:
        super().__init__(iterable)

        for trans in self:
            if type(trans) is not Translation:
                raise TypeError

    @classmethod
    def from_file(
        cls,
        file: _types.StrOrBytesPath,
        *,
        encoding: str | None = "utf-8",
        errors: str | None = None,
    ) -> typing.Self:
        with open(file, mode="rt", encoding=encoding, errors=errors, newline="") as f:
            try:
                return cls._from_io(f)
            except LanguageTSVError as exc:
                exc.file = file
                raise

    @classmethod
    def from_str(cls, s: str) -> typing.Self:
        f = io.StringIO(initial_value=s, newline="")
        return cls._from_io(f)

    @classmethod
    def _from_io(cls, f: io.TextIOWrapper) -> typing.Self:
        reader = csv.reader(f, dialect=LanguageTSVDialect)
        try:
            try:
                header = next(reader, None)
                if header != ["id", "description", "en", "local"]:
                    raise LanguageTSVError("invalid header")

                trans_list = []
                for record in reader:
                    if len(record) != 4:
                        raise LanguageTSVError("invalid number of fields")
                    trans = Translation(*record)
                    trans_list.append(trans)
            except csv.Error as exc:
                raise LanguageTSVError(str(exc)) from exc
        except LanguageTSVError as exc:
            exc.line = reader.line_num
            raise
        return cls(trans_list)

    def find_id(self, id: str) -> Translation:
        trans_list = self.find_id_all(id)
        if len(trans_list) <= 0:
            raise LanguageFindIDError(id)
        return trans_list[0]

    def find_id_all(self, id: str) -> list[Translation]:
        if type(id) is not str:
            raise TypeError
        return [trans for trans in self if trans.id == id]

    def find_en(self, en: str) -> Translation:
        trans_list = self.find_en_all(en)
        if len(trans_list) <= 0:
            raise LanguageFindEnError(en)
        return trans_list[0]

    def find_en_all(self, en: str) -> list[Translation]:
        if type(en) is not str:
            raise TypeError
        return [trans for trans in self if trans.en == en]
