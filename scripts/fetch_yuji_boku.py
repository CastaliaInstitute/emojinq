#!/usr/bin/env python3
"""Fetch the OFL-licensed Yuji Boku base font used for alpha source geometry."""

from pathlib import Path
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/yujiboku/"
TARGET = Path(".cache/base-font")


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in ("YujiBoku-Regular.ttf", "OFL.txt"):
        with urlopen(BASE + name, timeout=30) as response:
            (TARGET / name).write_bytes(response.read())
    print(f"fetched Yuji Boku into {TARGET}")


if __name__ == "__main__":
    main()
