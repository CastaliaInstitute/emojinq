#!/usr/bin/env python3
"""Check the browser-to-ledger label-blind evidence workflow."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "recognition.html"
IMPORTER = ROOT / "scripts" / "import_pua_recognition_session.py"
LEDGER = ROOT / "assets" / "pua-recognition-review.json"


def load_importer():
    spec = importlib.util.spec_from_file_location("recognition_importer", IMPORTER)
    if spec is None or spec.loader is None:
        raise SystemExit("could not load recognition-session importer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    page = PAGE.read_text(encoding="utf-8")
    required = (
        "32 CSS pixels",
        'width:32px; height:32px',
        'image.alt = ""',
        'glyph.className = current.variant === "color" ? "color-font" : "ink-font"',
        "String.fromCodePoint(...item.codepoints)",
        "Expected labels stay hidden until every trial is finished",
        "crypto.randomUUID()",
        "crypto.getRandomValues",
        'variant:"ink"',
        'variant:"color"',
        "family:current.family",
        "ink_sha256:current.ink_sha256",
        "color_sha256:current.color_sha256",
        'method:"label-blind-object-scale-review"',
        "localStorage.setItem(STORAGE_KEY",
        'item.status === "pending"',
        '`${item.id}:${item.status}:${item.ink_sha256}:${item.color_sha256}`',
        "Share this assigned-set link",
        'assignment.value.match(/^set:',
        'String(Number(match[1]) + 1)',
        'Number(requestedSet) - 1',
        'rejected awaiting redraw',
        "Export signed session JSON",
        "import_pua_recognition_session.py --write",
    )
    missing = [token for token in required if token not in page]
    if missing:
        raise SystemExit(f"recognition runner wiring missing: {', '.join(missing)}")
    if 'item.status !== "approved"' in page:
        raise SystemExit("recognition runner still offers unchanged rejected artwork for retest")
    scripts = re.findall(r"<script>(.*?)</script>", page, re.DOTALL)
    if len(scripts) != 1:
        raise SystemExit("recognition runner must contain exactly one inline script")
    node = shutil.which("node")
    if node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as script:
            script.write(scripts[0])
            script.flush()
            subprocess.run([node, "--check", script.name], check=True)

    assembler = (ROOT / "scripts" / "assemble_site.py").read_text(encoding="utf-8")
    gallery = (ROOT / "docs" / "all.html").read_text(encoding="utf-8")
    if "pua-recognition-review.json" not in assembler:
        raise SystemExit("Pages artifact does not copy the recognition ledger")
    if "recognition-session-link" not in gallery:
        raise SystemExit("gallery does not link to the structured recognition runner")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    current = ledger["items"][0]
    session = {
        "version": 1,
        "session_id": "workflow-self-test",
        "method": "label-blind-object-scale-review",
        "reviewer": "workflow self-test",
        "observer_age_months": 24,
        "label_hidden": True,
        "choice_free": True,
        "review_scale_css_px": 32,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "items": [
            {
                "id": current["id"],
                "family": current["family"],
                "source": current["source"],
                "expected": current["expected"],
                "ink_sha256": current["ink_sha256"],
                "color_sha256": current["color_sha256"],
                "color_mode": current["color_mode"],
                "ink_recognized_as": "verbatim ink guess",
                "color_recognized_as": "verbatim color guess",
                "status": "approved",
                "notes": "self-test only",
            }
        ],
    }
    importer = load_importer()
    ledger_by_id = {item["id"]: item for item in ledger["items"]}
    validated = importer.validate_session(session, ledger_by_id, Path("self-test.json"))
    if len(validated) != 1 or validated[0]["status"] != "approved":
        raise SystemExit("valid recognition-session fixture did not validate")
    for field, invalid in (
        ("observer_age_months", 48),
        ("label_hidden", False),
        ("choice_free", False),
        ("review_scale_css_px", 96),
    ):
        bad = deepcopy(session)
        bad[field] = invalid
        try:
            importer.validate_session(bad, ledger_by_id, Path("bad.json"))
        except ValueError:
            pass
        else:
            raise SystemExit(f"recognition importer accepted invalid {field}")
    stale = deepcopy(session)
    stale["items"][0]["ink_sha256"] = "0" * 64
    try:
        importer.validate_session(stale, ledger_by_id, Path("stale.json"))
    except ValueError:
        pass
    else:
        raise SystemExit("recognition importer accepted stale art hashes")
    completed_ledger = deepcopy(ledger_by_id)
    completed_ledger[current["id"]]["status"] = "approved"
    try:
        importer.validate_session(session, completed_ledger, Path("duplicate.json"))
    except ValueError:
        pass
    else:
        raise SystemExit("recognition importer accepted an overwrite of non-pending evidence")
    families = {item["family"] for item in ledger["items"]}
    if families != {"gray-all", "pua"}:
        raise SystemExit(f"recognition ledger family scope is incomplete: {sorted(families)}")
    print(f"recognition workflow checked: {len(ledger['items'])} standard and PUA hash-bound candidates, runner and importer valid")


if __name__ == "__main__":
    main()
