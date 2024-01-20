import os
import typing


StrOrBytesPath: typing.TypeAlias = str | bytes | os.PathLike[str] | os.PathLike[bytes]


def is_pathlike(v: object) -> typing.TypeGuard[StrOrBytesPath]:
    return type(v) is str or type(v) is bytes or isinstance(v, os.PathLike)
