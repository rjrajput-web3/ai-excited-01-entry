# Golden-Hour Whale — ai-excited-01

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/rjrajput-web3/ai-excited-01-entry/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/rjrajput-web3/ai-excited-01-entry/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

A humpback whale breaches clean out of the water at golden hour, right above a city skyline — spray catching the low sun, glass towers glowing amber below, the whole frame frozen at the peak of the leap. It is the one moment in the day when something enormous and wild shows up in the middle of ordinary city life, and the image is built to land that jolt of awe at first glance.

## How to run

```sh
python3 main.py
```

That copies `entry.png` to `/output/entry.png`. To choose a different
output folder, pass `--output <dir>` or set `MAKEFUN_OUTPUT_DIR`.

```sh
python3 main.py --output ./out
MAKEFUN_OUTPUT_DIR=./out python3 main.py
```

Python 3 only, standard library only — no network, no extra packages.

## How the output is verified

`main.py` checks `entry.png` is a real, complete PNG (magic bytes, a
13-byte IHDR first chunk, a zero-length IEND chunk at the end) before it
writes anything. It then writes the copy atomically (temp file +
`os.replace`) and compares SHA-256 hashes of the source and the written
file — the run prints the hash and only succeeds when they match. You can
check it yourself:

```sh
sha256sum entry.png /output/entry.png
```

Both hashes must be identical.
