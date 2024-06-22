#!/usr/bin/env python3

import argparse
import pathlib
import subprocess
import sys


def main() -> None:
    argp = argparse.ArgumentParser(allow_abbrev=False)
    argp.add_argument("--check", action="store_true")
    argv = argp.parse_args()
    argv_check: bool = argv.check

    repo_dir = pathlib.Path(__file__).parent

    script_file = pathlib.Path(repo_dir, "run_test.py")
    args = [sys.executable, script_file]
    result = subprocess.run(args)
    if result.returncode != 0:
        sys.exit(result.returncode)

    script_file = pathlib.Path(repo_dir, "run_update.py")
    args = [sys.executable, script_file]
    if argv_check:
        args.append("--check")
    result = subprocess.run(args)
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
