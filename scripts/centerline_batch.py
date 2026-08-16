#!/usr/bin/env python3
"""Batch the reviewed centerline recovery filter into a staging directory."""

from __future__ import annotations

import argparse
import concurrent.futures
import shutil
from pathlib import Path

from centerline_svg import emit, trace


def convert(source: Path, output: Path, threshold: int, minimum: float, speckle: int) -> tuple[str, int, str | None]:
    try:
        marks = trace(source, size=256, threshold=threshold, minimum=minimum, speckle=speckle)
        if not marks:
            return source.name, 0, "no centerline marks"
        emit(source, output, marks, source.stem, None)
        return source.name, len(marks), None
    except Exception as exc:  # keep one difficult glyph from stopping the queue
        return source.name, 0, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--only", nargs="*", help="specific source filenames to stage")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--threshold", type=int, default=220)
    parser.add_argument("--minimum", type=float, default=.65)
    parser.add_argument("--speckle", type=int, default=3)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="return a failure when any source glyph cannot be recovered",
    )
    args = parser.parse_args()
    if args.clean and args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sources = [args.source_dir / name for name in args.only] if args.only else sorted(args.source_dir.glob("*.svg"))
    sources = [source for source in sources if source.is_file()]
    print(f"staging {len(sources)} source SVGs with {max(1, args.jobs)} workers")
    failures: list[tuple[str, str]] = []
    completed = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {
            pool.submit(convert, source, args.output_dir / source.name, args.threshold, args.minimum, args.speckle): source
            for source in sources
        }
        for future in concurrent.futures.as_completed(futures):
            name, marks, error = future.result()
            completed += 1
            if error:
                failures.append((name, error))
            if completed % 100 == 0 or completed == len(sources):
                print(f"  {completed}/{len(sources)} complete; {len(failures)} failures")
    if failures:
        failure_file = args.output_dir / "centerline-failures.txt"
        failure_file.write_text("\n".join(f"{name}\t{error}" for name, error in sorted(failures)) + "\n")
        print(f"staged with {len(failures)} failures; see {failure_file}")
        if args.fail_on_error:
            raise SystemExit(f"centerline recovery failed for {len(failures)} glyphs")
    else:
        print(f"staged {len(sources)} stroke-only SVGs")


if __name__ == "__main__":
    main()
