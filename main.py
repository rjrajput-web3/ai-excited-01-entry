"""ai-excited-01 entry program.

Writes the entry image to the output directory. The image itself
(entry.png: a colossal humpback whale breaching through a city skyline at
golden hour) was generated procedurally during the build; this program only
places its exact bytes at the harness location, so every run produces
byte-identical output.

Standard library only. No network, no randomness, no timestamps.
"""

import os
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(source, "rb") as src:
        data = src.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    with open(dest, "wb") as out:
        out.write(data)
    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
