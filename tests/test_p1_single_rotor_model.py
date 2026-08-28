import math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"models"))
from p1_single_rotor_model import SolidDiskRotor,P1Limits,evaluate

def test_reference_geometry():
    r=SolidDiskRotor()
    assert math.isclose(r.mass_kg,0.5089380099,rel_tol=1e-9)
    assert math.isclose(r.inertia_kg_m2,0.0025446900,rel_tol=1e-7)

def test_energy_limit():
    result=evaluate()
    assert 31 < result["energy_at_command_j"] < 32
    assert result["energy_at_overspeed_j"] < 40
    assert result["passes_energy_limit"]

def test_rim_speed():
    r=SolidDiskRotor()
    assert math.isclose(r.rim_speed_m_s(1500),15.70796327,rel_tol=1e-8)

def test_energy_quadratic():
    r=SolidDiskRotor()
    assert math.isclose(r.energy_j(1000)*4,r.energy_j(2000),rel_tol=1e-12)
