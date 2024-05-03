import collections.abc
import csv
import dataclasses
import io
import os
import typing

from . import _types
from . import container
from . import wraperr


@dataclasses.dataclass
class Text:
    _: dataclasses.KW_ONLY
    id: str | None = None
    en: str = ""


@dataclasses.dataclass(frozen=True)
class Translation:
    id: str
    description: str
    en: str
    local: str


class LanguageTSVDialect(csv.Dialect):
    delimiter = "\t"
    doublequote = False
    escapechar = None
    lineterminator = "\n"
    quoting = csv.QUOTE_NONE
    skipinitialspace = False
    strict = True


class LanguageTSVError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: typing.Final[str] = msg
        self.file: _types.StrOrBytesPath | None = None
        self.line: int | None = None

    def __str__(self) -> str:
        file = os.fsdecode(self.file) if self.file is not None else None

        msg = self.msg
        if file is None and self.line is not None:
            msg = f"{self.msg} (at line {self.line!r})"
        if file is not None and self.line is None:
            msg = f"{self.msg} (in file '{file}')"
        if file is not None and self.line is not None:
            msg = f"{self.msg} (in file '{file}' at line {self.line!r})"
        return msg


class LanguageFindError(Exception):
    pass


class LanguageFindIDError(LanguageFindError):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.id: typing.Final[str] = id

    def __str__(self) -> str:
        return f"missing translation for id {self.id!r}"


class LanguageFindEnError(LanguageFindError):
    def __init__(self, en: str) -> None:
        super().__init__(en)
        self.en: typing.Final[str] = en

    def __str__(self) -> str:
        return f"missing translation for text {self.en!r}"


class Language(container.Sequence[Translation]):
    def __init__(self, iterable: collections.abc.Iterable[Translation] = ()) -> None:
        super().__init__(iterable=iterable)

        self._d_id: dict[str, list[Translation]] = {}
        self._d_en: dict[str, list[Translation]] = {}
        for trans in self:
            self._d_id.setdefault(trans.id, []).append(trans)
            self._d_en.setdefault(trans.en, []).append(trans)

    @classmethod
    def _from_io(cls, f: collections.abc.Iterable[str]) -> typing.Self:
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

    @classmethod
    def from_file(
        cls,
        file: _types.StrOrBytesPath,
        *,
        encoding: str | None = "utf-8",
        errors: str | None = None,
    ) -> typing.Self:
        with wraperr.wrap_unicode_error(file):
            with open(
                file, mode="rt", encoding=encoding, errors=errors, newline=""
            ) as f:
                try:
                    return cls._from_io(f)
                except LanguageTSVError as exc:
                    exc.file = file
                    raise

    @classmethod
    def from_str(cls, s: str) -> typing.Self:
        f = io.StringIO(initial_value=s, newline="")
        return cls._from_io(f)

    def find_id_all(self, id: str) -> list[Translation]:
        return self._d_id.get(id, [])[:]

    def find_id(self, id: str) -> Translation:
        trans_list = self.find_id_all(id)
        if len(trans_list) <= 0:
            raise LanguageFindIDError(id)
        return trans_list[0]

    def find_en_all(self, en: str) -> list[Translation]:
        return self._d_en.get(en, [])[:]

    def find_en(self, en: str) -> Translation:
        trans_list = self.find_en_all(en)
        if len(trans_list) <= 0:
            raise LanguageFindEnError(en)
        return trans_list[0]

    def translate(self, text: Text) -> str:
        if text.id is not None:
            trans = self.find_id(text.id)
        else:
            trans = self.find_en(text.en)
        return trans.local
