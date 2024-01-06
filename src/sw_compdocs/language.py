import csv
import io
import os

from . import container
from . import validator


class Language(container.Sequence):
    def __init__(self, iterable=()):
        super().__init__(iterable)

        for trans in self:
            if type(trans) is not Translation:
                raise TypeError

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

    def find_id(self, id, default=None):
        trans_list = self.find_id_all(id)

        trans = default
        if len(trans_list) > 0:
            trans = trans_list[0]
        return trans

    def find_id_all(self, id):
        if type(id) is not str:
            raise TypeError
        return [trans for trans in self if trans.id == id]

    def find_en(self, en, default=None):
        trans_list = self.find_en_all(en)

        trans = default
        if len(trans_list) > 0:
            trans = trans_list[0]
        return trans

    def find_en_all(self, en):
        if type(en) is not str:
            raise TypeError
        return [trans for trans in self if trans.en == en]


class Translation:
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) is not str:
            raise TypeError
        self._id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if type(value) is not str:
            raise TypeError
        self._description = value

    @property
    def en(self):
        return self._en

    @en.setter
    def en(self, value):
        if type(value) is not str:
            raise TypeError
        self._en = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, value):
        if type(value) is not str:
            raise TypeError
        self._local = value

    def __init__(self, id, description, en, local):
        self.id = id
        self.description = description
        self.en = en
        self.local = local

    def __repr__(self):
        return f"{type(self).__name__}({self.id!r}, {self.description!r}, {self.en!r}, {self.local!r})"

    def __eq__(self, other):
        if type(self) is type(other):
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
