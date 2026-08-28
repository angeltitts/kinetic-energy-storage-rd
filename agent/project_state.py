from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_FILES = ["PROJECT_BRIEF.md","REQUIREMENTS.md","ASSUMPTIONS.md","OPEN_QUESTIONS.md","DECISION_LOG.md","AGENT_CHARTER.md","CONFIDENCE_REGISTER.csv"]

@dataclass
class ProjectState:
    text: str

    @classmethod
    def load(cls) -> "ProjectState":
        blocks=[]
        for rel in STATE_FILES:
            path=ROOT/rel
            blocks.append(f"\n## {rel}\n" + (path.read_text(encoding="utf-8") if path.exists() else "[MISSING]") + "\n")
        for rel in ["results/baseline.json","results/latest_agent_report.md"]:
            path=ROOT/rel
            if path.exists():
                blocks.append(f"\n## {rel}\n" + path.read_text(encoding="utf-8") + "\n")
        return cls(text="\n".join(blocks))
