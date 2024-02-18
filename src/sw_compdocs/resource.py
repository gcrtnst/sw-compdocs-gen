import os
import re
import tomllib
import typing

from . import _types
from . import wraperr


class ResourceFileError(Exception):
    def __init__(self, msg: str, *, file: _types.StrOrBytesPath | None = None) -> None:
        super().__init__(msg)
        self.msg: typing.Final[str] = msg
        self.file: _types.StrOrBytesPath | None = file

    def __str__(self) -> str:
        msg = self.msg
        if self.file is not None:
            file = os.fsdecode(self.file)
            msg = f"{self.msg} (in file {file!r})"
        return msg


class TOMLFileDecodeError(tomllib.TOMLDecodeError):
    def __init__(
        self, *args: object, file: _types.StrOrBytesPath | None = None
    ) -> None:
        super().__init__(*args)
        self.file: _types.StrOrBytesPath | None = file

    def __str__(self) -> str:
        msg_list = []

        msg = super().__str__()
        if msg != "":
            msg_list.append(msg)

        if self.file is not None:
            file = os.fsdecode(self.file)
            msg_list.append(f"(in file {file!r})")

        msg_full = " ".join(msg_list)
        return msg_full


def format_toml_string(s: str) -> str:
    esc_set = frozenset(chr(i) for i in range(0x00, 0x20)) | {'"', "\\", "\x7F"}
    esc_dict = {
        "\b": r"\b",
        "\t": r"\t",
        "\n": r"\n",
        "\f": r"\f",
        "\r": r"\r",
        '"': r"\"",
        "\\": r"\\",
    }

    l = []
    for c in s:
        if c not in esc_set:
            l.append(c)
            continue
        if c in esc_dict:
            l.append(esc_dict[c])
            continue

        u = ord(c)
        if u <= 0xFFFF:
            l.append(f"\\u{u:04X}")
            continue
        l.append(f"\\U{u:08X}")
    return '"' + "".join(l) + '"'


def format_toml_key(key: str) -> str:
    if re.search(r"\A[A-Za-z0-9_\-]+\Z", key) is not None:
        return key
    return format_toml_string(key)


def load_toml_table(file: _types.StrOrBytesPath, table_key: str) -> dict[str, str]:
    try:
        with wraperr.wrap_unicode_error(filename=file):
            with open(file, mode="rb") as fp:
                toml: dict[str, object] = tomllib.load(fp)
    except tomllib.TOMLDecodeError as exc:
        exc_args: tuple[object, ...] = exc.args
        raise TOMLFileDecodeError(*exc_args, file=file) from exc

    obj = toml.get(table_key)
    if obj is None:
        exc_table_key = format_toml_key(table_key)
        exc_msg = f"table {exc_table_key!r} does not exist"
        raise ResourceFileError(exc_msg, file=file)
    if not isinstance(obj, dict):
        exc_table_key = format_toml_key(table_key)
        exc_obj_type = type(obj).__name__
        exc_msg = f"expected table for {exc_table_key!r}, but found {exc_obj_type}"
        raise ResourceFileError(exc_msg, file=file)

    # dict[typing.Any, typing.Any] -> dict[object, object]
    obj = typing.cast(dict[object, object], obj)

    table = {}
    for key, val in obj.items():
        if not isinstance(key, str):
            # In TOML, keys are always strings.
            # If a non-string key is given, it is a bug in tomllib.
            raise Exception
        if not isinstance(val, str):
            exc_key_1 = format_toml_key(table_key)
            exc_key_2 = format_toml_key(key)
            exc_key = exc_key_1 + "." + exc_key_2
            exc_val_type = type(val).__name__
            exc_msg = f"expected string value for {exc_key!r}, but found {exc_val_type}"
            raise ResourceFileError(exc_msg, file=file)
        table[key] = val
    return table
