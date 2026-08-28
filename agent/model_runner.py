from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_model(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        check=True,
        cwd=str(ROOT / "models"),
    )
    return result.stdout[-8000:]


def run_models() -> str:
    system_model = ROOT / "models" / "system_model.py"
    sweep_model = ROOT / "models" / "parameter_sweep.py"

    if not system_model.exists():
        return "system_model.py missing."

    baseline_stdout = _run_model(system_model)

    blocks = []
    if sweep_model.exists():
        blocks.append("\n\nPARAMETER SWEEP\n" + _run_model(sweep_model))

    for header, filename in [
        ("PHASE 1 FEASIBILITY", "phase1_feasibility.py"),
        ("PHASE 2 MASS BUDGET", "phase2_mass_budget.py"),
        ("PHASE 3 SEGMENTED CONTAINMENT", "phase3_segmented_containment.py"),
    ]:
        path = ROOT / "models" / filename
        if path.exists():
            blocks.append(f"\n\n{header}\n" + _run_model(path))

    baseline = ROOT / "results" / "baseline.json"
    baseline_text = baseline.read_text(encoding="utf-8") if baseline.exists() else ""

    return (
        "BASELINE MODEL STDOUT\n"
        + baseline_stdout[-8000:]
        + "\n\nBASELINE JSON\n"
        + baseline_text[-8000:]
        + "".join(blocks)
    )
