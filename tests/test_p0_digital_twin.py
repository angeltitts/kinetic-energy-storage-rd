import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P0 = ROOT / "prototype" / "p0"
sys.path.insert(0, str(P0))

from digital_twin import AnnularRotor, P0DigitalTwin


def test_reference_rotor_energy_is_low():
    twin = P0DigitalTwin()
    assert math.isclose(twin.total_rotor_energy_at_300rpm_j, 1.625, rel_tol=0.02)


def test_differential_tracking():
    twin = P0DigitalTwin()
    twin.run_constant((180, 120, 60), 60.0, dt=0.01)
    for measured, target in zip(twin.rpms, (180, 120, 60)):
        assert abs(measured - target) / target < 0.05


def test_command_clamps_to_300rpm():
    twin = P0DigitalTwin()
    state = twin.step((500, 10, 10), 0.01)
    assert state["target_rpm"][0] == 300.0


def test_vibration_fault_latches_and_stays_latched():
    twin = P0DigitalTwin()
    twin.step((100, 100, 100), 0.01, vibration_g=1.2)
    assert twin.fault_latched
    assert twin.fault_reason == "vibration"
    twin.step((0, 0, 0), 0.01)
    assert twin.fault_latched


def test_rotor_properties_match_build_spec_order():
    rotor = AnnularRotor(0.300, 0.270, 0.006)
    assert 0.09 < rotor.mass_kg < 0.11
    assert rotor.inertia_kg_m2 > 0
