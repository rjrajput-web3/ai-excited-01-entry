"""Entry program for the make.fun ai-excited-01 bounty.

The artwork lives beside this file as entry.png. All this program
does is place an exact copy of it at the output location the grader
reads, so every run produces the same bytes.
"""

import os
import shutil
from pathlib import Path


def entry_image_path() -> Path:
    """Return the artwork file sitting next to this program."""
    return Path(__file__).resolve().parent / "entry.png"


def output_path() -> Path:
    """Return where the image must land.

    The grader sets MAKEFUN_OUTPUT_DIR; otherwise fall back to the
    standard /output directory used by the competition sandbox.
    """
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(folder) / "entry.png"


def main() -> None:
    source = entry_image_path()
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise RuntimeError("copied image size does not match the source")
    print(f"Wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
