import pytest

from prototype.p1_single_rotor.overspeed_gate import (
    OVERSPEED_RPM,
    PULSES_PER_REV,
    evaluate,
    period_to_rpm,
)


def test_period_mapping_for_12_slot_target():
    assert period_to_rpm(60.0 / (1500.0 * PULSES_PER_REV)) == pytest.approx(1500.0)
    assert period_to_rpm(60.0 / (1650.0 * PULSES_PER_REV)) == pytest.approx(1650.0)


def test_overspeed_trips_at_threshold():
    decision = evaluate(OVERSPEED_RPM, 0.001, OVERSPEED_RPM)
    assert not decision.permit
    assert decision.latched_fault
    assert decision.reason == "overspeed"


def test_just_below_threshold_allowed():
    assert evaluate(1649.0, 0.001, 1649.0).permit


def test_stale_fails_closed_after_motion_seen():
    decision = evaluate(0.0, 0.251, 0.0, motion_seen=True)
    assert not decision.permit
    assert decision.reason == "independent_rpm_stale"


def test_stationary_start_does_not_false_trip_stale_gate():
    assert evaluate(0.0, 1.0, 0.0, motion_seen=False).permit


def test_disagreement_fails_closed():
    assert evaluate(1400.0, 0.001, 1500.0).reason == "rpm_disagreement"


def test_latch_persists():
    assert evaluate(0.0, 0.0, 0.0, prior_latched=True).reason == "latched_fault"


def test_invalid_inputs():
    with pytest.raises(ValueError):
        period_to_rpm(0.0)
    with pytest.raises(ValueError):
        evaluate(-1.0, 0.0, 0.0)
