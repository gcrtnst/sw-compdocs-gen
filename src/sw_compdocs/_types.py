import os
import typing


type StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]


def is_pathlike(v: object) -> typing.TypeGuard[StrOrBytesPath]:
    return isinstance(v, str) or isinstance(v, bytes) or isinstance(v, os.PathLike)
