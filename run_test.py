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
    result = subprocess.run(["pyflakes", "--"] + src_list)
    warn = warn or result.returncode != 0

    print("==> Running black")
    result = subprocess.run(["black", "--check", "--quiet", "--"] + src_list)
    warn = warn or result.returncode != 0

    print("==> Running mypy")
    # Run mypy with the --no-incremental flag to ensure all errors are reported.
    result = subprocess.run(
        ["mypy", "--no-incremental", "--no-error-summary", "--"] + src_list
    )
    warn = warn or result.returncode != 0

    print("==> Running unittest")
    result = subprocess.run(
        [
            "python",
            "-m",
            "unittest",
            "discover",
            "--quiet",
            "--start-directory",
            str(repo_dir),
        ]
    )
    warn = warn or result.returncode != 0

    print("==> " + ("FAIL" if warn else "PASS"))
    sys.exit(1 if warn else 0)


if __name__ == "__main__":
    main()
