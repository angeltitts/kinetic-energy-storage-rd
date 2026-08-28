import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from phase1_feasibility import (
    required_effective_stress_gpa,
    system_whkg,
    tip_speed_m_s,
)


def test_required_stress_closes_target():
    target = 500.0
    density = 1500.0
    overhead = 0.60
    stress = required_effective_stress_gpa(target, density, overhead)
    assert math.isclose(system_whkg(stress, density, overhead), target, rel_tol=1e-12)


def test_more_overhead_requires_more_stress():
    a = required_effective_stress_gpa(500.0, 1500.0, 0.4)
    b = required_effective_stress_gpa(500.0, 1500.0, 0.8)
    assert b > a


def test_tip_speed_is_multikilometer_per_second_at_gate():
    stress = required_effective_stress_gpa(500.0, 1500.0, 0.6)
    assert tip_speed_m_s(stress, 1500.0) > 2000.0
