#!/usr/bin/env python3
"""Validate and import real label-blind recognition-session exports.

The browser session is deliberately unable to edit the release ledger.  This
tool is the review boundary: it rejects stale art hashes, incomplete protocol
fields, unknown sources, and unadjudicated observations before updating the
hash-bound ledger.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "assets" / "pua-recognition-review.json"
VALID_STATUSES = {"approved", "rejected"}


def text(value: object) -> str:
    return str(value or "").strip()


def valid_timestamp(value: object) -> bool:
    try:
        datetime.fromisoformat(text(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_session(session: dict, ledger_by_source: dict[str, dict], source_file: Path) -> list[dict]:
    errors: list[str] = []
    reviewer = text(session.get("reviewer"))
    session_id = text(session.get("session_id"))
    completed_at = session.get("completed_at")
    age = session.get("observer_age_months")
    if session.get("method") != "label-blind-object-scale-review":
        errors.append("method must be label-blind-object-scale-review")
    if not reviewer:
        errors.append("reviewer is required")
    if not session_id:
        errors.append("session_id is required")
    if not valid_timestamp(completed_at):
        errors.append("completed_at must be an ISO-8601 timestamp")
    if not isinstance(age, int) or not 12 <= age <= 47:
        errors.append("observer_age_months must be an integer from 12 through 47")
    if session.get("label_hidden") is not True:
        errors.append("label_hidden must be true")
    if session.get("choice_free") is not True:
        errors.append("choice_free must be true")
    if session.get("review_scale_css_px") != 32:
        errors.append("review_scale_css_px must be 32")
    raw_items = session.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        errors.append("items must be a non-empty array")
        raw_items = []

    seen: set[str] = set()
    validated: list[dict] = []
    for index, item in enumerate(raw_items, 1):
        if not isinstance(item, dict):
            errors.append(f"item {index} must be an object")
            continue
        source = text(item.get("source"))
        prefix = source or f"item {index}"
        current = ledger_by_source.get(source)
        if current is None:
            errors.append(f"{prefix}: source is not in the current recognition ledger")
            continue
        if source in seen:
            errors.append(f"{prefix}: duplicate source in session")
            continue
        seen.add(source)
        for field in ("expected", "ink_sha256", "color_sha256", "color_mode"):
            if item.get(field) != current.get(field):
                errors.append(f"{prefix}: stale or mismatched {field}")
        status = item.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{prefix}: status must be approved or rejected")
        ink_guess = text(item.get("ink_recognized_as"))
        color_guess = text(item.get("color_recognized_as"))
        if not ink_guess or not color_guess:
            errors.append(f"{prefix}: both verbatim guesses are required")
        validated.append(
            {
                "source": source,
                "status": status,
                "reviewer": reviewer,
                "reviewed_at": text(completed_at),
                "ink_recognized_as": ink_guess,
                "color_recognized_as": color_guess,
                "evidence": f"recognition-session:{source_file.name}#{session_id}",
                "notes": text(item.get("notes")),
                "observer_age_months": age,
                "label_hidden": True,
                "choice_free": True,
                "review_scale_css_px": 32,
            }
        )
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    return validated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", type=Path, nargs="+", help="exported recognition-session JSON")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--write", action="store_true", help="write validated observations to the ledger")
    args = parser.parse_args()

    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    ledger_by_source = {item["source"]: item for item in ledger.get("items", [])}
    updates: dict[str, dict] = {}
    for session_path in args.sessions:
        session = json.loads(session_path.read_text(encoding="utf-8"))
        try:
            validated = validate_session(session, ledger_by_source, session_path)
        except ValueError as error:
            raise SystemExit(f"invalid recognition session {session_path}:\n{error}") from error
        for update in validated:
            source = update["source"]
            if source in updates:
                raise SystemExit(f"source appears in multiple input sessions: {source}")
            updates[source] = update

    approved = sum(update["status"] == "approved" for update in updates.values())
    rejected = len(updates) - approved
    if not args.write:
        print(
            f"validated {len(updates)} observations ({approved} approved, {rejected} rejected); "
            "ledger unchanged (pass --write to import)"
        )
        return
    for source, update in updates.items():
        ledger_by_source[source].update(update)
    args.ledger.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"imported {len(updates)} observations ({approved} approved, {rejected} rejected)")


if __name__ == "__main__":
    main()
