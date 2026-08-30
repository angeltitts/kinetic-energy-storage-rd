import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "models"))

from hybrid_power_buffer import (
    DispatchConfig,
    HybridLimits,
    HybridState,
    battery_peak_reduction,
    dispatch_step,
)


LIMITS = HybridLimits(
    battery_discharge_w=5000,
    battery_charge_w=3000,
    flywheel_discharge_w=5000,
    flywheel_charge_w=5000,
)


def test_flywheel_takes_step_transient():
    state = HybridState(battery_power_w=0.0, flywheel_soc=0.5)
    batt, fw = dispatch_step(
        4000,
        state,
        LIMITS,
        DispatchConfig(alpha=0.05, soc_target=0.5, soc_gain_w=0),
    )
    assert batt < 500
    assert fw > 3500


def test_regen_prefers_flywheel_when_headroom_exists():
    state = HybridState(battery_power_w=0.0, flywheel_soc=0.5)
    batt, fw = dispatch_step(
        -3000,
        state,
        LIMITS,
        DispatchConfig(alpha=0.05, soc_target=0.5, soc_gain_w=0),
    )
    assert fw < -2500
    assert abs(batt) < 500


def test_low_flywheel_soc_blocks_discharge():
    state = HybridState(battery_power_w=0.0, flywheel_soc=0.1)
    batt, fw = dispatch_step(
        2000,
        state,
        LIMITS,
        DispatchConfig(alpha=0.05, soc_target=0.5, soc_gain_w=0),
    )
    assert fw == 0
    assert batt == 2000


def test_peak_reduction_metric():
    r = battery_peak_reduction([0, 100, -100], [0, 40, -40])
    assert abs(r - 0.6) < 1e-12
