import collections.abc
import csv
import io
import os

from . import validator


class Language(collections.abc.Mapping):
    def __init__(self):
        super().__init__()
        self._d = {}

    @classmethod
    def from_file(cls, file, *, encoding="utf-8", errors=None):
        with open(file, mode="rt", encoding=encoding, errors=errors, newline="") as f:
            try:
                return cls._from_io(f)
            except LanguageTSVError as exc:
                exc.file = file
                raise

    @classmethod
    def from_str(cls, s):
        f = io.StringIO(initial_value=s, newline="")
        return cls._from_io(f)

    @classmethod
    def _from_io(cls, f):
        reader = csv.reader(f, dialect=LanguageTSVDialect)
        try:
            try:
                header = next(reader, None)
                if header != ["id", "description", "en", "local"]:
                    raise LanguageTSVError("invalid header")

                d = {}
                for record in reader:
                    if len(record) != 4:
                        raise LanguageTSVError("invalid number of fields")
                    d[record[2]] = record[3]
            except csv.Error as exc:
                raise LanguageTSVError(str(exc)) from exc
        except LanguageTSVError as exc:
            exc.line = reader.line_num
            raise

        lang = cls()
        lang._d = d
        return lang

    def __getitem__(self, key):
        try:
            return self._d[key]
        except KeyError:
            raise LanguageKeyError(key)

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)


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
    def msg(self):
        return self._msg

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if value is not None and not validator.is_pathlike(value):
            raise TypeError
        self._file = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        if value is not None and type(value) is not int:
            raise TypeError
        self._line = value

    def __init__(self, msg):
        if type(msg) is not str:
            raise TypeError

        super().__init__(msg)
        self._msg = msg
        self._file = None
        self._line = None

    def __str__(self):
        file = os.fsdecode(self.file) if self.file is not None else "<language.tsv>"
        line = str(self.line) if self.line is not None else "?"
        return f"{file}: line {line}: {self.msg}"


class LanguageKeyError(KeyError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key

    def __str__(self):
        return f"missing translation for {repr(self.key)}"
