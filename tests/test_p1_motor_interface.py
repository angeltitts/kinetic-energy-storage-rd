import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from motor_interface import MotorFaceMeasurement, required_plate_margin_mm


def test_four_holes_are_equally_spaced_on_measured_circle():
    m = MotorFaceMeasurement(4, 38.0, 4.5, 16.0)
    holes = m.hole_centers_mm()
    radii = [math.hypot(x, y) for x, y in holes]
    assert all(math.isclose(r, 19.0, abs_tol=1e-12) for r in radii)
    assert len(holes) == 4


def test_released_plate_has_margin_for_reference_measured_pattern():
    m = MotorFaceMeasurement(4, 38.0, 4.5, 16.0)
    assert required_plate_margin_mm(m) > 0


def test_oversize_pattern_is_detected_before_machining():
    m = MotorFaceMeasurement(4, 80.0, 5.0, 16.0)
    assert required_plate_margin_mm(m) < 0


def test_invalid_center_clearance_overlap_is_rejected():
    m = MotorFaceMeasurement(4, 20.0, 5.0, 16.0)
    try:
        m.validate()
    except ValueError:
        pass
    else:
        raise AssertionError("overlapping geometry must be rejected")
