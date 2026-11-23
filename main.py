"""Entry program for news-image-20261122 (Python 3.13, standard library).

Copies the front-page image entry.png sitting next to this file into the
output directory the grader provides, so the judge sees exactly the image
this repository holds. Deterministic: the same input bytes are written on
every run.
"""

import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / "entry.png")
    print("wrote " + str(out_dir / "entry.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
