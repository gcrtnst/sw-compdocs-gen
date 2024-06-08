#!/usr/bin/env python3

import pathlib
import sw_compdocs.resource
import tomli_w
import tomllib


def _dump_toml(toml_dict: dict[str, dict[str, str]], toml_file: pathlib.Path) -> None:
    # tomli-w may not generate valid TOML. Validate output with tomllib.
    tomllib.loads(tomli_w.dumps(toml_dict))

    with open(toml_file, mode="wb") as fp:
        tomli_w.dump(toml_dict, fp)


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
