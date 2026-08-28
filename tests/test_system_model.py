import math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"models"))
from system_model import Material,Rotor,SystemMassModel,evaluate,tip_speed_m_s

def test_thin_ring_relation():
    m=Material(1500.0,20e9,1.0,1.0); v=tip_speed_m_s(m)
    assert math.isclose(v*v*m.density_kg_m3,20e9,rel_tol=1e-12)
def test_radius_changes_rpm_not_tip_speed():
    m=Material(); r1=evaluate(m,Rotor(radius_m=0.25),SystemMassModel()); r2=evaluate(m,Rotor(radius_m=1.0),SystemMassModel())
    assert math.isclose(r1["tip_speed_m_s"],r2["tip_speed_m_s"],rel_tol=1e-12); assert r1["rpm"]>r2["rpm"]
def test_system_whkg_lower_than_rotor_whkg():
    r=evaluate(); assert r["system_specific_energy_Wh_kg"]<r["rotor_specific_energy_Wh_kg"]
