import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from supervisor import (  # noqa: E402
    P1Supervisor,
    P1SupervisorLimits,
    SupervisorSample,
    rotor_rpm_to_erpm,
    rotor_rpm_to_motor_rpm,
)


def test_drive_mapping_matches_released_15_to_48_ratio():
    assert math.isclose(rotor_rpm_to_motor_rpm(1500.0), 4800.0, rel_tol=1e-12)


def test_command_and_overspeed_erpm_are_below_vesc_limit():
    assert math.isclose(rotor_rpm_to_erpm(1500.0), 33600.0, rel_tol=1e-12)
    assert math.isclose(rotor_rpm_to_erpm(1650.0), 36960.0, rel_tol=1e-12)
    assert rotor_rpm_to_erpm(1650.0) < 60000.0


def test_independent_overspeed_latches_at_released_threshold():
    ctl = P1Supervisor()
    ctl.update_independent_sensor_timestamp(1.0)
    assert ctl.evaluate(SupervisorSample(1.0, 1650.0, 1640.0, True))
    assert ctl.latched
    assert ctl.reason == "independent_overspeed"


def test_below_overspeed_does_not_trip_when_sensors_agree():
    ctl = P1Supervisor()
    ctl.update_independent_sensor_timestamp(1.0)
    assert not ctl.evaluate(SupervisorSample(1.0, 1500.0, 1490.0, True))
    assert not ctl.latched


def test_sensor_staleness_latches_during_commanded_run():
    ctl = P1Supervisor()
    ctl.update_independent_sensor_timestamp(1.0)
    assert ctl.evaluate(SupervisorSample(1.251, 1200.0, 1200.0, True))
    assert ctl.reason == "independent_sensor_stale"


def test_sensor_disagreement_above_five_percent_latches():
    ctl = P1Supervisor()
    ctl.update_independent_sensor_timestamp(2.0)
    assert ctl.evaluate(SupervisorSample(2.0, 1000.0, 1060.0, True))
    assert ctl.reason == "rpm_sensor_disagreement"


def test_fault_remains_latched_until_reset():
    ctl = P1Supervisor()
    ctl.update_independent_sensor_timestamp(0.0)
    assert ctl.evaluate(SupervisorSample(0.0, 1700.0, 1700.0, True))
    assert ctl.evaluate(SupervisorSample(0.1, 0.0, 0.0, False))
    ctl.reset()
    assert not ctl.latched


def test_limits_preserve_released_envelope():
    limits = P1SupervisorLimits()
    assert limits.command_rpm == 1500.0
    assert limits.overspeed_rpm == 1650.0
