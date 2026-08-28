from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _impact_weight(value: str) -> float:
    return {
        "critical": 4.0,
        "high": 3.0,
        "medium": 2.0,
        "low": 1.0,
    }.get(value.strip().lower(), 1.0)


def select_highest_value_task() -> dict[str, str]:
    path = ROOT / "CONFIDENCE_REGISTER.csv"
    if not path.exists():
        return {
            "claim_id": "BOOTSTRAP",
            "claim": "Establish the first quantitative feasibility result.",
            "next_action": "Run and interpret the Phase 0 model.",
            "tie_note": "",
        }

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise RuntimeError("CONFIDENCE_REGISTER.csv contains no claims.")

    def score(row):
        confidence = float(row.get("confidence_percent") or 50.0)
        return max(0.0, 100.0 - confidence) * _impact_weight(
            row.get("impact") or "medium"
        )

    scored = sorted(
        ((score(row), index, row) for index, row in enumerate(rows)),
        key=lambda item: (-item[0], item[1]),
    )
    top_score = scored[0][0]
    tied = [row for s, _index, row in scored if s == top_score]
    selected = dict(scored[0][2])

    if len(tied) > 1:
        claim_ids = ", ".join(row.get("claim_id", "[unknown]") for row in tied)
        selected["tie_note"] = (
            f"Top task-selection score {top_score:g} is tied by: {claim_ids}. "
            f"Deterministic row order selected {selected.get('claim_id')}."
        )
    else:
        selected["tie_note"] = ""

    return selected
