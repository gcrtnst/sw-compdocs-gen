import re


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
