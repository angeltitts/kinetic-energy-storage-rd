from __future__ import annotations

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentConfig:
    model: str = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    max_tasks_per_run: int = int(os.getenv("MAX_AGENT_TASKS_PER_RUN", "1"))
    max_output_chars: int = int(os.getenv("MAX_AGENT_OUTPUT_CHARS", "20000"))

    def validate(self) -> None:
        if self.max_tasks_per_run < 1 or self.max_tasks_per_run > 3:
            raise ValueError("MAX_AGENT_TASKS_PER_RUN must be between 1 and 3.")
        if self.max_output_chars < 2000:
            raise ValueError("MAX_AGENT_OUTPUT_CHARS is too small.")
