import collections.abc
import contextlib
import os
import typing


from . import _types


class UnicodeEncodeFileError(UnicodeEncodeError):
    def __init__(
        self,
        __encoding: str,
        __object: str,
        __start: int,
        __end: int,
        __reason: str,
        *,
        filename: _types.StrOrBytesPath | None = None,
    ) -> None:
        super().__init__(__encoding, __object, __start, __end, __reason)
        self.filename: _types.StrOrBytesPath | None = filename

    @classmethod
    def extends(
        cls, exc: UnicodeEncodeError, filename: _types.StrOrBytesPath
    ) -> typing.Self:
        return cls(
            exc.encoding, exc.object, exc.start, exc.end, exc.reason, filename=filename
        )

    def __str__(self) -> str:
        if self.filename is None:
            return super().__str__()

        filename = os.fsdecode(self.filename)
        if self.start < len(self.object) and self.end == self.start + 1:
            badchar = ord(self.object[self.start])
            if badchar <= 0xFF:
                return f"'{self.encoding}' codec can't encode character '\\x{badchar:02x}' in file '{filename}': {self.reason}"
            if badchar <= 0xFFFF:
                return f"'{self.encoding}' codec can't encode character '\\u{badchar:04x}' in file '{filename}': {self.reason}"
            return f"'{self.encoding}' codec can't encode character '\\U{badchar:08x}' in file '{filename}': {self.reason}"
        return f"'{self.encoding}' codec can't encode characters in file '{filename}': {self.reason}"


class UnicodeDecodeFileError(UnicodeDecodeError):
    def __init__(
        self,
        __encoding: str,
        __object: bytes,
        __start: int,
        __end: int,
        __reason: str,
        *,
        filename: _types.StrOrBytesPath | None = None,
    ) -> None:
        super().__init__(__encoding, __object, __start, __end, __reason)
        self.filename: _types.StrOrBytesPath | None = filename

    @classmethod
    def extends(
        cls, exc: UnicodeDecodeError, filename: _types.StrOrBytesPath
    ) -> typing.Self:
        return cls(
            exc.encoding, exc.object, exc.start, exc.end, exc.reason, filename=filename
        )

    def __str__(self) -> str:
        if self.filename is None:
            return super().__str__()

        filename = os.fsdecode(self.filename)
        if self.start < len(self.object) and self.end == self.start + 1:
            byte = self.object[self.start]
            return f"'{self.encoding}' codec can't decode byte 0x{byte:02x} in file '{filename}': {self.reason}"
        return f"'{self.encoding}' codec can't decode bytes in file '{filename}': {self.reason}"


class UnicodeTranslateFileError(UnicodeTranslateError):
    def __init__(
        self,
        __object: str,
        __start: int,
        __end: int,
        __reason: str,
        *,
        filename: _types.StrOrBytesPath | None = None,
    ) -> None:
        super().__init__(__object, __start, __end, __reason)
        self.filename: _types.StrOrBytesPath | None = filename

    @classmethod
    def extends(
        cls, exc: UnicodeTranslateError, filename: _types.StrOrBytesPath
    ) -> typing.Self:
        return cls(exc.object, exc.start, exc.end, exc.reason, filename=filename)

    def __str__(self) -> str:
        if self.filename is None:
            return super().__str__()

        filename = os.fsdecode(self.filename)
        if self.start < len(self.object) and self.end == self.start + 1:
            badchar = ord(self.object[self.start])
            if badchar <= 0xFF:
                return f"can't translate character '\\x{badchar:02x}' in file '{filename}': {self.reason}"
            if badchar <= 0xFFFF:
                return f"can't translate character '\\u{badchar:04x}' in file '{filename}': {self.reason}"
            return f"can't translate character '\\U{badchar:08x}' in file '{filename}': {self.reason}"
        return f"can't translate characters in file '{filename}': {self.reason}"


@contextlib.contextmanager
def wrap_unicode_error(
    filename: _types.StrOrBytesPath,
) -> collections.abc.Iterator[None]:
    try:
        yield None
    except UnicodeEncodeFileError as exc:
        exc.filename = filename
        raise
    except UnicodeDecodeFileError as exc:
        exc.filename = filename
        raise
    except UnicodeTranslateFileError as exc:
        exc.filename = filename
        raise
    except UnicodeEncodeError as exc:
        raise UnicodeEncodeFileError.extends(exc, filename) from exc
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeFileError.extends(exc, filename) from exc
    except UnicodeTranslateError as exc:
        raise UnicodeTranslateFileError.extends(exc, filename) from exc
