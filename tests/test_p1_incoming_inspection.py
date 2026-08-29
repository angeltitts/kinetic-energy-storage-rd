import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from incoming_inspection import IncomingInspection, evaluate


def valid_record(**overrides):
    data = dict(
        motor_bolt_count=4,
        motor_bolt_circle_mm=38.0,
        motor_hole_diameter_mm=4.0,
        motor_center_clearance_mm=12.0,
        shaft_diameter_mm=12.0,
        bearing_bore_mm=12.0,
        pulley_runout_mm=0.05,
        rotor_radial_runout_mm=0.12,
        rotor_axial_wobble_mm=0.10,
        shaft_bearing_fit_ok=True,
        pulley_runout_disposition_ok=True,
    )
    data.update(overrides)
    return IncomingInspection(**data)


def test_valid_incoming_inspection_passes():
    passed, reasons = evaluate(valid_record())
    assert passed
    assert reasons == []


def test_released_radial_runout_limit_is_enforced():
    passed, reasons = evaluate(valid_record(rotor_radial_runout_mm=0.251))
    assert not passed
    assert any("radial runout" in reason for reason in reasons)


def test_released_axial_wobble_limit_is_enforced():
    passed, reasons = evaluate(valid_record(rotor_axial_wobble_mm=0.251))
    assert not passed
    assert any("axial wobble" in reason for reason in reasons)


def test_missing_measurement_fails_closed():
    passed, reasons = evaluate(valid_record(pulley_runout_mm=None))
    assert not passed
    assert "pulley_runout_mm missing/invalid" in reasons


def test_purchased_part_fit_requires_explicit_disposition():
    passed, reasons = evaluate(valid_record(shaft_bearing_fit_ok=False))
    assert not passed
    assert "shaft_bearing_fit_ok not confirmed" in reasons


def test_pulley_runout_requires_explicit_disposition_without_invented_limit():
    passed, reasons = evaluate(valid_record(pulley_runout_disposition_ok=None))
    assert not passed
    assert "pulley_runout_disposition_ok not confirmed" in reasons
