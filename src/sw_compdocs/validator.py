import os
import typing

from . import _types


def is_pathlike(v: object) -> typing.TypeGuard[_types.StrOrBytesPath]:
    return type(v) is str or type(v) is bytes or isinstance(v, os.PathLike)
