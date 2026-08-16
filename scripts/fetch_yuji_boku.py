#!/usr/bin/env python3
"""Fetch the OFL-licensed Yuji families used for alpha source geometry."""

from pathlib import Path
from urllib.request import urlopen

TARGET = Path(".cache/base-font")


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    for family, filename in (
        ("yujiboku", "YujiBoku-Regular.ttf"),
        ("yujimai", "YujiMai-Regular.ttf"),
        ("yujisyuku", "YujiSyuku-Regular.ttf"),
    ):
        base = f"https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/"
        with urlopen(base + filename, timeout=30) as response:
            (TARGET / filename).write_bytes(response.read())
    with urlopen("https://raw.githubusercontent.com/google/fonts/main/ofl/yujisyuku/OFL.txt", timeout=30) as response:
        (TARGET / "OFL.txt").write_bytes(response.read())
    print(f"fetched Yuji families into {TARGET}")


if __name__ == "__main__":
    main()
