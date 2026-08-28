import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from phase3_segmented_containment import (
    ReferenceCase,
    required_catcher_sea_mjkg,
    required_hoop_count,
)


def test_one_hoop_failure_count_at_half_mjkg_catcher():
    case = ReferenceCase()
    assert required_hoop_count(case, 0.5, 1) == 39


def test_five_hoop_cascade_scales_count():
    case = ReferenceCase()
    assert required_hoop_count(case, 0.5, 5) == 193


def test_required_sea_falls_with_more_segments():
    case = ReferenceCase()
    assert required_catcher_sea_mjkg(case, 100, 1) < required_catcher_sea_mjkg(case, 20, 1)
