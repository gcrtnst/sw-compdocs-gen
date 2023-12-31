import os


def is_pathlike(v):
    return type(v) is str or type(v) is bytes or isinstance(v, os.PathLike)
