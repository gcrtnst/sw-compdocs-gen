#!/usr/bin/env python3

import argparse
import pathlib
import subprocess
import sys


def main() -> None:
    argp = argparse.ArgumentParser(allow_abbrev=False)
    argp.parse_args()

    warn = False
    repo_dir = pathlib.Path(__file__).parent
    pyproject_file = pathlib.Path(repo_dir, "pyproject.toml")

    print("==> Running ruff check", flush=True)
    args = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        "--config",
        str(pyproject_file),
        "--no-fix",
        "--",
        str(repo_dir),
    ]
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running ruff format", flush=True)
    args = [
        sys.executable,
        "-m",
        "ruff",
        "format",
        "--config",
        str(pyproject_file),
        "--check",
        "--",
        str(repo_dir),
    ]
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running pyright", flush=True)
    args = [
        sys.executable,
        "-m",
        "pyright",
        "--project",
        str(pyproject_file),
        "--pythonpath",
        sys.executable,
    ]
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running unittest", flush=True)
    args = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "--start-directory",
        str(repo_dir),
    ]
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> " + ("FAIL" if warn else "PASS"), flush=True)
    sys.exit(1 if warn else 0)


if __name__ == "__main__":
    main()
