#!/usr/bin/env python3

import pathlib
import subprocess
import sys


def main() -> None:
    warn = False
    repo_dir = pathlib.Path(__file__).parent

    src_list = []
    for pattern in ["*.py", "src/**/*.py", "tests/**/*.py"]:
        for src_file in repo_dir.glob(pattern):
            if src_file.is_file():
                src_list.append(str(src_file))
    src_list.sort()

    print("==> Running pyflakes")
    args = [sys.executable, "-m", "pyflakes", "--"] + src_list
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running black")
    args = [sys.executable, "-m", "black", "--check", "--"] + src_list
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running mypy")
    # Run mypy with the --no-incremental flag to ensure all errors are reported.
    args = [sys.executable, "-m", "mypy", "--no-incremental", "--"] + src_list
    result = subprocess.run(args)
    warn = warn or result.returncode != 0

    print("==> Running unittest")
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

    print("==> " + ("FAIL" if warn else "PASS"))
    sys.exit(1 if warn else 0)


if __name__ == "__main__":
    main()
