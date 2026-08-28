from __future__ import annotations

import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run_models()->str:
    system_model=ROOT/"models"/"system_model.py"
    sweep_model=ROOT/"models"/"parameter_sweep.py"
    if not system_model.exists():
        return "system_model.py missing."
    b=subprocess.run([sys.executable,str(system_model)],capture_output=True,text=True,check=True,cwd=str(ROOT/"models"))
    sweep_text=""
    if sweep_model.exists():
        s=subprocess.run([sys.executable,str(sweep_model)],capture_output=True,text=True,check=True,cwd=str(ROOT/"models"))
        sweep_text="\n\nPARAMETER SWEEP\n"+s.stdout[-8000:]
    baseline=ROOT/"results"/"baseline.json"
    baseline_text=baseline.read_text(encoding="utf-8") if baseline.exists() else ""
    return "BASELINE MODEL STDOUT\n"+b.stdout[-8000:]+"\n\nBASELINE JSON\n"+baseline_text[-8000:]+sweep_text
