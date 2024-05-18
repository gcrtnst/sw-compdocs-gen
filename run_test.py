#!/usr/bin/env python3

import pathlib
import shutil
import subprocess
import sys


def main() -> None:
    warn = False
    repo_dir = pathlib.Path(__file__).parent
    pyproject_file = pathlib.Path(repo_dir, "pyproject.toml")

    src_list: list[str] = []
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

    print("==> Running pyright")
    pyright = shutil.which("pyright")
    if pyright is None:
        print("pyright is not found in PATH")
        warn = True
    else:
        args = [
            pyright,
            "--project",
            str(pyproject_file),
            "--pythonpath",
            sys.executable,
        ]
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
