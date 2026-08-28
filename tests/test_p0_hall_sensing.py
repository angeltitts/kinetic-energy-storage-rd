import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p0"))

from hall_sensing import (  # noqa: E402
    PULSES_PER_REV,
    STALE_TIMEOUT_S,
    is_stale,
    pulse_period_s,
    rpm_from_period_s,
)


def test_release_uses_four_pulses_per_rev():
    assert PULSES_PER_REV == 4


def test_acceptance_speed_pulse_periods_fit_timeout():
    # All P0 acceptance speeds must produce at least two pulses before the
    # stale timeout expires. This leaves margin for scheduler/jitter delay.
    for rpm in (50, 60, 100, 120, 150, 180, 200, 300):
        period = pulse_period_s(rpm)
        assert 2.0 * period <= STALE_TIMEOUT_S


def test_50_rpm_has_300ms_pulse_spacing():
    assert math.isclose(pulse_period_s(50), 0.30, rel_tol=0, abs_tol=1e-9)


def test_60_rpm_has_250ms_pulse_spacing():
    assert math.isclose(pulse_period_s(60), 0.25, rel_tol=0, abs_tol=1e-9)


def test_period_conversion_round_trip():
    for rpm in (50, 60, 100, 180, 300, 330):
        assert math.isclose(rpm_from_period_s(pulse_period_s(rpm)), rpm, rel_tol=1e-12)


def test_stale_timeout_behavior():
    assert not is_stale(STALE_TIMEOUT_S)
    assert is_stale(STALE_TIMEOUT_S + 1e-6)


def test_prior_one_pulse_design_would_fail_50rpm_timeout():
    prior_period = pulse_period_s(50, pulses_per_rev=1)
    assert prior_period == 1.2
    assert prior_period > 1.0
