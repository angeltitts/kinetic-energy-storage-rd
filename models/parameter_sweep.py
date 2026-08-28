from __future__ import annotations
import csv,itertools
from pathlib import Path
from system_model import Material,Rotor,SystemMassModel,evaluate
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=[]
    for strength,fd,sf,radius,c,scale in itertools.product([10,15,20,25,30,40],[0.4,0.5,0.6,0.7],[1.25,1.5,2.0],[0.25,0.5,1.0],[0.25,0.5,0.75,1.0,1.5,2.0],[0.5,0.75,1.0]):
        material=Material(1500.0,strength*1e9,fd,sf); rotor=Rotor(50.0,radius)
        masses=SystemMassModel(c,0.15*scale,0.20*scale,0.08*scale,0.08*scale,0.10*scale,0.03*scale)
        r=evaluate(material,rotor,masses)
        rows.append({"strength_GPa":strength,"fatigue_derating":fd,"safety_factor":sf,"radius_m":radius,"containment_ratio":c,"other_parasitic_scale":scale,"effective_stress_GPa":r["effective_stress_GPa"],"tip_speed_m_s":r["tip_speed_m_s"],"rpm":r["rpm"],"rotor_Wh_kg":r["rotor_specific_energy_Wh_kg"],"system_Wh_kg":r["system_specific_energy_Wh_kg"],"stored_kWh":r["stored_energy_kWh"],"total_mass_kg":r["total_system_mass_kg"],"passes_500":r["passes_500_Wh_kg"]})
    rows.sort(key=lambda x:x["system_Wh_kg"],reverse=True)
    out=ROOT/"results"/"phase0_sweep.csv"; out.parent.mkdir(exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"Wrote {len(rows)} cases to {out}")
    print("Best candidate:")
    for k,v in rows[0].items(): print(f"{k}: {v}")
if __name__=="__main__": main()
