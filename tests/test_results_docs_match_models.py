import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from phase1_feasibility import Target, build_rows as phase1_rows
from phase2_mass_budget import Case, max_containment_ratio, max_total_nonrotor_ratio
from phase3_segmented_containment import ReferenceCase, required_hoop_count


def test_phase1_markdown_reference_row():
    row = next(
        r
        for r in phase1_rows(Target())
        if math.isclose(r["total_nonrotor_mass_per_rotor_mass"], 0.60)
    )
    assert math.isclose(row["required_effective_stress_GPa"], 8.64, abs_tol=0.005)
    assert math.isclose(
        row["required_fatigue_retention_at_SF1p5"] * 100.0,
        64.8,
        abs_tol=0.05,
    )
    assert math.isclose(row["required_tip_speed_m_s"] / 1000.0, 2.40, abs_tol=0.005)


def test_phase2_markdown_reference_row():
    case = Case(fatigue_retention=0.65)
    assert math.isclose(max_total_nonrotor_ratio(case), 0.605, abs_tol=0.0005)
    assert math.isclose(max_containment_ratio(case, 0.45), 0.155, abs_tol=0.0005)


def test_phase3_markdown_reference_row():
    assert required_hoop_count(ReferenceCase(), 0.5, 1) == 39
