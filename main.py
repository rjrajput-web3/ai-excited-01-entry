#!/usr/bin/env python3
"""ai-excited-01 entry: copy the judged whale-breach image to the output dir.

The image itself (entry.png, a golden-hour whale breaching over a city
skyline) is the entry's artwork. This program only validates that it is a
real, complete PNG and copies its exact bytes to the output directory, so
the judge always sees the identical image that was submitted.
"""

import argparse
import hashlib
import os
import sys
import tempfile

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IHDR_MARKER = b"IHDR"
IEND_MARKER = b"IEND"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_png(data, path):
    """Reject anything that is not a complete PNG file.

    Parses the real chunk structure instead of just searching for markers:
    the first chunk must be a 13-byte IHDR, and the file must end with a
    zero-length IEND chunk (length + type + CRC).
    """
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        fail(f"{path} is not a PNG file (bad magic bytes)")
    if len(data) < 8 + 8 + 13 + 12:
        fail(f"{path} is too small to be a complete PNG")
    first_length = int.from_bytes(data[8:12], "big")
    first_type = data[12:16]
    if first_type != IHDR_MARKER or first_length != 13:
        fail(f"{path} is not a PNG file (first chunk is not a 13-byte IHDR)")
    if data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != IEND_MARKER:
        fail(f"{path} looks truncated (no zero-length IEND chunk at the end)")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Copy entry.png to the output directory after "
                    "validating it is a complete PNG.")
    parser.add_argument(
        "--output", default=None,
        help="output directory (overrides MAKEFUN_OUTPUT_DIR, "
             "default /output)")
    args = parser.parse_args(argv)

    output_dir = args.output or os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, "entry.png")
    if not os.path.isfile(source_path):
        fail(f"entry.png not found next to main.py ({source_path})")

    with open(source_path, "rb") as handle:
        data = handle.read()

    check_png(data, source_path)
    source_hash = sha256_hex(data)

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        fail(f"could not create output directory {output_dir}: {exc}")

    dest_path = os.path.join(output_dir, "entry.png")

    # Atomic write: build the copy in a temp file inside the output
    # directory, then swap it into place, so a reader never sees a
    # half-written image.
    fd, tmp_path = tempfile.mkstemp(prefix=".entry-", dir=output_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        with open(tmp_path, "rb") as handle:
            written_hash = sha256_hex(handle.read())
        if written_hash != source_hash:
            fail("SHA-256 mismatch after writing the copy; refusing to publish it")
        os.replace(tmp_path, dest_path)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    with open(dest_path, "rb") as handle:
        final_hash = sha256_hex(handle.read())
    if final_hash != source_hash:
        fail("SHA-256 mismatch on the final file; output is not identical")

    print(f"wrote {dest_path} ({len(data)} bytes)")
    print(f"SHA-256: {final_hash} (matches source)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
