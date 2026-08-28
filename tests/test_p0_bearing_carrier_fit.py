from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p0"))

from bearing_carrier_fit import (  # noqa: E402
    BEARING,
    ROTOR_IDS_MM,
    radial_clearance_to_rotor_id_mm,
    validate_bearing_carrier_envelope,
)


def test_four_inch_bearing_fits_inside_every_rotor_id():
    result = validate_bearing_carrier_envelope()
    assert result["bearing_fits_all_rotor_ids"]
    assert result["smallest_rotor_clearance_mm"] == 24.0


def test_nominal_bearing_thickness_fits_reserved_stack_allowance():
    assert BEARING.thickness_mm <= BEARING.maximum_stack_allowance_mm


def test_clearance_decreases_with_rotor_id():
    clearances = [radial_clearance_to_rotor_id_mm(ROTOR_IDS_MM[name]) for name in ("A", "B", "C")]
    assert clearances == [84.0, 54.0, 24.0]


def test_oversize_bearing_is_rejected_by_smallest_rotor():
    assert radial_clearance_to_rotor_id_mm(150.0, bearing_envelope_mm=152.0) < 0
