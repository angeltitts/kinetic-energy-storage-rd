import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from phase2_mass_budget import Case, max_total_nonrotor_ratio, max_containment_ratio


def test_65pct_fatigue_case_total_budget():
    case = Case(fatigue_retention=0.65)
    assert math.isclose(max_total_nonrotor_ratio(case), 0.6049382716049381, rel_tol=1e-12)


def test_containment_budget_is_residual():
    case = Case(fatigue_retention=0.65)
    assert math.isclose(max_containment_ratio(case, 0.45), 0.15493827160493812, rel_tol=1e-12)


def test_low_fatigue_retention_can_eliminate_containment_budget():
    case = Case(fatigue_retention=0.55)
    assert max_containment_ratio(case, 0.45) < 0
