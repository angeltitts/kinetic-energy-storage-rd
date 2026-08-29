import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from acceptance_analyzer import (
    CycleMetrics,
    coefficient_of_variation_percent,
    evaluate_acceptance,
    summarize_cycle,
)
from instrumentation import Sample


def _cycle(recovered: float, coast: float, *, faulted=False, moved=False):
    return CycleMetrics(
        charge_energy_j=40.0,
        recovered_energy_j=recovered,
        round_trip_efficiency=recovered / 40.0,
        coastdown_time_s=coast,
        peak_vibration_g=0.03,
        witness_mark_moved=moved,
        faulted=faulted,
    )


def test_five_repeatable_cycles_pass():
    cycles = [_cycle(20.0 + 0.4 * i, 60.0 + i) for i in range(5)]
    result = evaluate_acceptance(cycles)
    assert result.passed
    assert result.recovered_energy_cv_percent < 10.0
    assert result.coastdown_time_cv_percent < 10.0


def test_recovered_energy_variation_over_limit_fails():
    cycles = [_cycle(20.0, 60.0) for _ in range(4)] + [_cycle(35.0, 60.0)]
    result = evaluate_acceptance(cycles)
    assert not result.passed
    assert result.recovered_energy_cv_percent >= 10.0
    assert any("recovered-energy CV" in reason for reason in result.reasons)


def test_fault_and_witness_movement_fail():
    cycles = [_cycle(20.0, 60.0) for _ in range(4)] + [
        _cycle(20.0, 60.0, faulted=True, moved=True)
    ]
    result = evaluate_acceptance(cycles)
    assert not result.passed
    assert any("faulted" in reason for reason in result.reasons)
    assert any("witness-mark" in reason for reason in result.reasons)


def test_fewer_than_five_cycles_cannot_pass():
    result = evaluate_acceptance([_cycle(20.0, 60.0) for _ in range(4)])
    assert not result.passed
    assert result.recovered_energy_cv_percent is None


def test_summarize_cycle_uses_bus_sign_convention_and_vibration_peak():
    charge = [
        Sample(0.0, 300, 20.0, 1.0, 0.02),
        Sample(2.0, 1500, 20.0, 1.0, 0.04),
    ]
    regen = [
        Sample(0.0, 1500, 20.0, -0.8, 0.03),
        Sample(2.0, 300, 20.0, -0.8, 0.05),
    ]
    metrics = summarize_cycle(charge, regen, 60.0)
    assert math.isclose(metrics.charge_energy_j, 40.0, rel_tol=1e-12)
    assert math.isclose(metrics.recovered_energy_j, 32.0, rel_tol=1e-12)
    assert math.isclose(metrics.round_trip_efficiency, 0.8, rel_tol=1e-12)
    assert math.isclose(metrics.peak_vibration_g, 0.05, rel_tol=1e-12)


def test_cv_reference_values_are_stable():
    recovered = [20.0, 20.4, 20.8, 21.2, 21.6]
    coast = [60.0, 61.0, 62.0, 63.0, 64.0]
    assert math.isclose(coefficient_of_variation_percent(recovered), 2.7196, rel_tol=1e-3)
    assert math.isclose(coefficient_of_variation_percent(coast), 2.2810, rel_tol=1e-3)
