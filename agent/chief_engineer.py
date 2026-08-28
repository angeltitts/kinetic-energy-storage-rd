from __future__ import annotations

import os
from pathlib import Path
from openai import OpenAI
from agent.config import AgentConfig
from agent.model_runner import run_models
from agent.project_state import ProjectState
from agent.prompts import CHIEF_ENGINEER_SYSTEM, build_cycle_prompt
from agent.task_selector import select_highest_value_task

ROOT=Path(__file__).resolve().parents[1]

def run_one_cycle()->str:
    config=AgentConfig(); config.validate()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not configured. Run deterministic models locally or configure the GitHub secret.")
    state=ProjectState.load(); task=select_highest_value_task(); model_summary=run_models()
    client=OpenAI()
    response=client.responses.create(model=config.model,instructions=CHIEF_ENGINEER_SYSTEM,input=build_cycle_prompt(state.text,task,model_summary),reasoning={"effort":"high"})
    report=response.output_text.strip()
    if len(report)>config.max_output_chars:
        report=report[:config.max_output_chars]+"\n\n[TRUNCATED]\n"
    out=ROOT/"results"/"latest_agent_report.md"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("# Autonomous Engineering Cycle Report\n\n"+report+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    print(run_one_cycle())
