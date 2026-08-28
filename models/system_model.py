"""Phase 0 DSHC feasibility model. Analytical screening only."""
from dataclasses import dataclass,asdict
import json,math
from pathlib import Path
J_PER_WH=3600.0
ROOT=Path(__file__).resolve().parents[1]
@dataclass
class Material:
    density_kg_m3:float=1500.0
    tensile_strength_pa:float=20e9
    fatigue_derating:float=0.50
    safety_factor:float=1.50
    @property
    def effective_stress_pa(self): return self.tensile_strength_pa*self.fatigue_derating/self.safety_factor
@dataclass
class Rotor:
    mass_kg:float=50.0
    radius_m:float=0.50
@dataclass
class SystemMassModel:
    containment_ratio:float=0.75
    vacuum_housing_ratio:float=0.15
    stator_ratio:float=0.20
    bearing_ratio:float=0.08
    cryogenic_ratio:float=0.08
    power_electronics_ratio:float=0.10
    controls_ratio:float=0.03

def rotor_specific_energy_j_kg(m): return m.effective_stress_pa/(2.0*m.density_kg_m3)
def rotor_specific_energy_wh_kg(m): return rotor_specific_energy_j_kg(m)/J_PER_WH
def tip_speed_m_s(m): return math.sqrt(m.effective_stress_pa/m.density_kg_m3)
def rpm(m,radius_m):
    if radius_m<=0: raise ValueError("radius_m must be positive")
    return (tip_speed_m_s(m)/radius_m)*60.0/(2.0*math.pi)
def evaluate(material=None,rotor=None,masses=None):
    material=material or Material(); rotor=rotor or Rotor(); masses=masses or SystemMassModel()
    rotor_whkg=rotor_specific_energy_wh_kg(material); stored_wh=rotor_whkg*rotor.mass_kg
    ratios=asdict(masses); parasitic_ratio=sum(ratios.values()); parasitic_mass=parasitic_ratio*rotor.mass_kg
    total_mass=rotor.mass_kg+parasitic_mass; system_whkg=stored_wh/total_mass
    return {"material":asdict(material),"rotor":asdict(rotor),"mass_model":ratios,"effective_stress_GPa":material.effective_stress_pa/1e9,"tip_speed_m_s":tip_speed_m_s(material),"rpm":rpm(material,rotor.radius_m),"rotor_specific_energy_Wh_kg":rotor_whkg,"stored_energy_kWh":stored_wh/1000.0,"parasitic_mass_kg":parasitic_mass,"total_system_mass_kg":total_mass,"system_specific_energy_Wh_kg":system_whkg,"passes_500_Wh_kg":system_whkg>=500.0}
if __name__=="__main__":
    result=evaluate(); out=ROOT/"results"/"baseline.json"; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(result,indent=2),encoding="utf-8"); print(json.dumps(result,indent=2))
