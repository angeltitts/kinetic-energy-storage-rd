import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.rotordynamics.whirl_model import RotorDynamicsModel
from cad.generator import export_phase1


def specific_energy_whkg(strength_pa, density):
    return strength_pa / (2.0 * density) / 3600.0


def test_carbon_fiber_specific_energy():
    assert math.isclose(specific_energy_whkg(7e9, 1800), 540.12345679, rel_tol=1e-6)


def test_tip_speed_relation():
    strength = 7e9
    density = 1800.0
    v = math.sqrt(strength / density)
    assert v <= math.sqrt(strength / density)


def test_radial_expansion_below_clearance_at_selected_rpm():
    model = RotorDynamicsModel(
        outer_diameter_m=0.30,
        radial_thickness_m=0.002,
        material_density_kg_m3=1800.0,
        hoop_tensile_modulus_gpa=230.0,
        k_r_n_m=2.0e6,
        k_z_n_m=3.0e6,
    )
    expansion = model.check_uncoupled_ring_expansion(30000.0)
    assert expansion["radial_growth_m"] < 0.0005


def test_cad_exports(tmp_path):
    exported = export_phase1(tmp_path)
    assert exported
    for path in exported.values():
        assert path.exists()
        assert path.stat().st_size > 100
