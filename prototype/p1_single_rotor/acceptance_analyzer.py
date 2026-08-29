from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Sequence

from instrumentation import Sample, integrate_bus_energy_j, round_trip_efficiency


MIN_CONSECUTIVE_REGEN_CYCLES = 5
MAX_REPEATABILITY_CV_PERCENT = 10.0


@dataclass(frozen=True)
class CycleMetrics:
    charge_energy_j: float
    recovered_energy_j: float
    round_trip_efficiency: float
    coastdown_time_s: float
    peak_vibration_g: float
    witness_mark_moved: bool = False
    faulted: bool = False


@dataclass(frozen=True)
class AcceptanceResult:
    passed: bool
    recovered_energy_cv_percent: float | None
    coastdown_time_cv_percent: float | None
    reasons: tuple[str, ...]


def coefficient_of_variation_percent(values: Sequence[float]) -> float:
    vals = [float(v) for v in values]
    if not vals:
        raise ValueError("values must not be empty")
    if any(v < 0 for v in vals):
        raise ValueError("values must be non-negative")
    mu = mean(vals)
    if mu <= 0:
        raise ValueError("mean must be positive")
    return pstdev(vals) / mu * 100.0


def summarize_cycle(
    charge_samples: Sequence[Sample],
    regen_samples: Sequence[Sample],
    coastdown_time_s: float,
    *,
    witness_mark_moved: bool = False,
    faulted: bool = False,
) -> CycleMetrics:
    if coastdown_time_s <= 0:
        raise ValueError("coastdown_time_s must be positive")
    charge_energy = integrate_bus_energy_j(charge_samples)
    regen_signed = integrate_bus_energy_j(regen_samples)
    recovered_energy = -regen_signed
    efficiency = round_trip_efficiency(charge_samples, regen_samples)
    peak_vibration = max(
        [s.vibration_g for s in charge_samples] + [s.vibration_g for s in regen_samples],
        default=0.0,
    )
    return CycleMetrics(
        charge_energy_j=charge_energy,
        recovered_energy_j=recovered_energy,
        round_trip_efficiency=efficiency,
        coastdown_time_s=coastdown_time_s,
        peak_vibration_g=peak_vibration,
        witness_mark_moved=witness_mark_moved,
        faulted=faulted,
    )


def evaluate_acceptance(cycles: Sequence[CycleMetrics]) -> AcceptanceResult:
    reasons: list[str] = []
    if len(cycles) < MIN_CONSECUTIVE_REGEN_CYCLES:
        return AcceptanceResult(
            passed=False,
            recovered_energy_cv_percent=None,
            coastdown_time_cv_percent=None,
            reasons=(f"need at least {MIN_CONSECUTIVE_REGEN_CYCLES} completed cycles",),
        )

    window = list(cycles[-MIN_CONSECUTIVE_REGEN_CYCLES:])

    if any(c.faulted for c in window):
        reasons.append("one or more of the last five cycles faulted")
    if any(c.recovered_energy_j <= 0 for c in window):
        reasons.append("one or more of the last five cycles returned no positive electrical energy")
    if any(c.witness_mark_moved for c in window):
        reasons.append("hub/shaft witness-mark movement observed")

    recovered_cv: float | None
    if all(c.recovered_energy_j > 0 for c in window):
        recovered_cv = coefficient_of_variation_percent(
            [c.recovered_energy_j for c in window]
        )
        if recovered_cv >= MAX_REPEATABILITY_CV_PERCENT:
            reasons.append(
                f"recovered-energy CV {recovered_cv:.2f}% is not below "
                f"{MAX_REPEATABILITY_CV_PERCENT:.1f}%"
            )
    else:
        recovered_cv = None

    coast_cv = coefficient_of_variation_percent([c.coastdown_time_s for c in window])
    if coast_cv >= MAX_REPEATABILITY_CV_PERCENT:
        reasons.append(
            f"coast-down-time CV {coast_cv:.2f}% is not below "
            f"{MAX_REPEATABILITY_CV_PERCENT:.1f}%"
        )

    return AcceptanceResult(
        passed=not reasons,
        recovered_energy_cv_percent=recovered_cv,
        coastdown_time_cv_percent=coast_cv,
        reasons=tuple(reasons),
    )
