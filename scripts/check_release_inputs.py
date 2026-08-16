#!/usr/bin/env python3
"""Check that release inputs and GitHub Pages CI remain reproducible."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    requirements = (ROOT / "requirements-build.txt").read_text(encoding="utf-8").splitlines()
    floating = [line for line in requirements if line.strip() and not line.lstrip().startswith("#") and "==" not in line]
    if floating:
        raise SystemExit(f"unpinned Python requirements: {', '.join(floating)}")

    fetcher = (ROOT / "scripts" / "fetch_openmoji.py").read_text(encoding="utf-8")
    if not re.search(r'PINNED_REF\s*=\s*"[0-9a-f]{40}"', fetcher):
        raise SystemExit("OpenMoji source is not pinned to a full commit SHA")

    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    required = (
        "make color-font",
        "make check",
        "make release-check",
        "make site",
        "dist/pages",
        "Emojinq-Color.ttf",
    )
    missing = [token for token in required if token not in workflow and token != "Emojinq-Color.ttf"]
    # The font name lives in the deterministic assembler, not duplicated YAML.
    assembler = (ROOT / "scripts" / "assemble_site.py").read_text(encoding="utf-8")
    if "Emojinq-Color.ttf" not in assembler:
        missing.append("Emojinq-Color.ttf")
    if missing:
        raise SystemExit(f"GitHub Pages release pipeline is incomplete: {', '.join(missing)}")
    action_uses = re.findall(r"^\s*uses:\s*([^\s#]+)", workflow, re.MULTILINE)
    unpinned_actions = [value for value in action_uses if not re.search(r"@[0-9a-f]{40}$", value)]
    if unpinned_actions:
        raise SystemExit(f"GitHub Actions are not SHA-pinned: {', '.join(unpinned_actions)}")
    print(f"release inputs checked: {len(requirements)} pinned Python packages, {len(action_uses)} pinned actions")


if __name__ == "__main__":
    main()
