from __future__ import annotations

from dataclasses import dataclass

from models.hybrid_power_buffer import DispatchConfig, HybridLimits, HybridState, dispatch_step


@dataclass(frozen=True)
class HilResult:
    battery_peak_w: float
    load_peak_w: float
    peak_reduction_fraction: float
    max_flywheel_abs_w: float
    final_flywheel_soc: float
    unmet_energy_j: float


def run_profile(
    load_series_w: list[float],
    dt_s: float,
    initial_soc: float,
    usable_flywheel_energy_j: float,
    limits: HybridLimits,
    cfg: DispatchConfig,
) -> HilResult:
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    if usable_flywheel_energy_j <= 0:
        raise ValueError("usable_flywheel_energy_j must be positive")

    state = HybridState(battery_power_w=0.0, flywheel_soc=initial_soc)
    batt: list[float] = []
    fw: list[float] = []
    unmet_energy_j = 0.0

    for load_w in load_series_w:
        batt_w, fw_w = dispatch_step(load_w, state, limits, cfg)
        served_w = batt_w + fw_w
        unmet_energy_j += abs(load_w - served_w) * dt_s

        # Positive flywheel power discharges stored energy; negative charges it.
        state.flywheel_soc -= fw_w * dt_s / usable_flywheel_energy_j
        state.flywheel_soc = max(0.0, min(1.0, state.flywheel_soc))
        state.battery_power_w = batt_w

        batt.append(batt_w)
        fw.append(fw_w)

    load_peak = max((abs(x) for x in load_series_w), default=0.0)
    batt_peak = max((abs(x) for x in batt), default=0.0)
    reduction = 0.0 if load_peak == 0 else 1.0 - batt_peak / load_peak

    return HilResult(
        battery_peak_w=batt_peak,
        load_peak_w=load_peak,
        peak_reduction_fraction=reduction,
        max_flywheel_abs_w=max((abs(x) for x in fw), default=0.0),
        final_flywheel_soc=state.flywheel_soc,
        unmet_energy_j=unmet_energy_j,
    )


def p1_reference_profile() -> list[float]:
    """Desktop-only profile representing pulses and regen, not a hardware command."""
    return (
        [0.0] * 20
        + [80.0] * 20
        + [0.0] * 20
        + [-50.0] * 10
        + [0.0] * 20
        + [100.0] * 20
        + [20.0] * 20
        + [-60.0] * 10
        + [0.0] * 20
    )
