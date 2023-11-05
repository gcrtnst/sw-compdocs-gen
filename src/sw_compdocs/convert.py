def as_str(v):
    if not isinstance(v, str):
        raise TypeError
    return str(v)
