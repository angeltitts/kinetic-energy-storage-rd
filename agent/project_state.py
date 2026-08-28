from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_FILES = [
    "PROJECT_BRIEF.md",
    "REQUIREMENTS.md",
    "ASSUMPTIONS.md",
    "OPEN_QUESTIONS.md",
    "DECISION_LOG.md",
    "AGENT_CHARTER.md",
    "ARCHITECTURE_GEN6.md",
    "CONFIDENCE_REGISTER.csv",
]


@dataclass
class ProjectState:
    text: str

    @classmethod
    def load(cls) -> "ProjectState":
        blocks = []
        for rel in STATE_FILES:
            path = ROOT / rel
            blocks.append(
                f"\n## {rel}\n"
                + (path.read_text(encoding="utf-8") if path.exists() else "[MISSING]")
                + "\n"
            )

        # results/baseline.json is the superseded conservative Phase-0 baseline:
        # it fails the 500 Wh/kg gate under fixed mass-ratio assumptions. The
        # Phase 1-3 result documents below are the current best analysis and
        # must be read alongside it rather than treated as older/lower-priority.
        result_files = [
            "results/baseline.json",
            "results/phase1_feasibility.md",
            "results/phase2_mass_budget.md",
            "results/phase3_segmented_containment.md",
            "results/latest_agent_report.md",
        ]
        for rel in result_files:
            path = ROOT / rel
            if path.exists():
                blocks.append(
                    f"\n## {rel}\n" + path.read_text(encoding="utf-8") + "\n"
                )

        return cls(text="\n".join(blocks))
