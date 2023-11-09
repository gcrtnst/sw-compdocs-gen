import collections.abc
import csv
import io


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
                raise LanguageTSVError(exc.msg, file=file, line=exc.line)

    @classmethod
    def from_str(cls, s):
        f = io.StringIO(initial_value=s, newline="")
        return cls._from_io(f)

    @classmethod
    def _from_io(cls, f):
        reader = csv.reader(f, dialect=LanguageTSVDialect)
        try:
            header = next(reader, None)
            if header != ["id", "description", "en", "local"]:
                raise LanguageTSVError("invalid header", line=reader.line_num)

            d = {}
            for record in reader:
                if len(record) != 4:
                    raise LanguageTSVError(
                        "invalid number of fields", line=reader.line_num
                    )
                d[record[2]] = record[3]
        except csv.Error as exc:
            raise LanguageTSVError(str(exc), line=reader.line_num)

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
    def __init__(self, msg, file=None, line=None):
        super().__init__(msg, file, line)
        self.msg = msg
        self.file = file
        self.line = line

    def __str__(self):
        file = str(self.file) if self.file is not None else "<language.tsv>"
        line = str(self.line) if self.line is not None else "?"
        return f"{file}: line {line}: {self.msg}"


class LanguageKeyError(KeyError):
    def __init__(self, key):
        super().__init__(key)
        self.key = key

    def __str__(self):
        return f"missing translation for {repr(self.key)}"
