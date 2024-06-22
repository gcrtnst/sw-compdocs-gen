#!/usr/bin/env python3

import io
import pathlib
import sw_compdocs.resource
import tomli_w
import tomllib


def _dump_toml(toml_dict: dict[str, dict[str, str]], toml_file: pathlib.Path) -> None:
    with io.BytesIO() as bio:
        tomli_w.dump(toml_dict, bio)
        toml_bin = bio.getvalue()

    with io.BytesIO(toml_bin) as bio:
        load_dict = tomllib.load(bio)
    if load_dict != toml_dict:
        raise Exception

    with open(toml_file, mode="wb") as fp:
        fp.write(toml_bin)


def main() -> None:
    repo_dir = pathlib.Path(__file__).parent

    toml_dict = {"label": dict(sw_compdocs.resource.default_label)}
    toml_file = pathlib.Path(repo_dir, "res/sw_compdocs_label.toml")
    _dump_toml(toml_dict, toml_file)

    toml_dict = {"keybindings": dict(sw_compdocs.resource.default_bind)}
    toml_file = pathlib.Path(repo_dir, "res/sw_compdocs_keybindings.toml")
    _dump_toml(toml_dict, toml_file)


if __name__ == "__main__":
    main()
