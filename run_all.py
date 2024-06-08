#!/usr/bin/env python3

import pathlib
import subprocess
import sys


def main() -> None:
    repo_dir = pathlib.Path(__file__).parent
    for script_name in ["run_test.py", "run_update.py"]:
        script_file = pathlib.Path(repo_dir, script_name)
        subprocess.run([sys.executable, script_file])


if __name__ == "__main__":
    main()
