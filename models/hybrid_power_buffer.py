from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HybridState:
    battery_power_w: float = 0.0
    flywheel_soc: float = 0.5


@dataclass(frozen=True)
class HybridLimits:
    battery_discharge_w: float
    battery_charge_w: float
    flywheel_discharge_w: float
    flywheel_charge_w: float
    flywheel_soc_min: float = 0.1
    flywheel_soc_max: float = 0.9


@dataclass(frozen=True)
class DispatchConfig:
    alpha: float = 0.05
    soc_target: float = 0.5
    soc_gain_w: float = 1000.0


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def dispatch_step(
    load_power_w: float,
    state: HybridState,
    limits: HybridLimits,
    cfg: DispatchConfig,
) -> tuple[float, float]:
    """Return (battery_power_w, flywheel_power_w).

    Positive = delivering power to the load.
    Negative = absorbing regenerative power.
    """

    batt_lp = state.battery_power_w + cfg.alpha * (
        load_power_w - state.battery_power_w
    )

    residual = load_power_w - batt_lp

    # If SOC is high, favor flywheel discharge.
    # If SOC is low, favor flywheel charging / reduced discharge.
    soc_bias = cfg.soc_gain_w * (state.flywheel_soc - cfg.soc_target)
    fw_cmd = residual + soc_bias

    if state.flywheel_soc <= limits.flywheel_soc_min and fw_cmd > 0:
        fw_cmd = 0.0
    if state.flywheel_soc >= limits.flywheel_soc_max and fw_cmd < 0:
        fw_cmd = 0.0

    fw_cmd = clamp(
        fw_cmd,
        -limits.flywheel_charge_w,
        limits.flywheel_discharge_w,
    )

    batt_cmd = load_power_w - fw_cmd
    batt_cmd = clamp(
        batt_cmd,
        -limits.battery_charge_w,
        limits.battery_discharge_w,
    )

    # Reconcile if battery clamping leaves unmet power.
    fw_cmd = load_power_w - batt_cmd
    fw_cmd = clamp(
        fw_cmd,
        -limits.flywheel_charge_w,
        limits.flywheel_discharge_w,
    )

    return batt_cmd, fw_cmd


def battery_peak_reduction(load_series_w, batt_series_w) -> float:
    load_peak = max(abs(x) for x in load_series_w)
    batt_peak = max(abs(x) for x in batt_series_w)
    if load_peak == 0:
        return 0.0
    return 1.0 - batt_peak / load_peak
