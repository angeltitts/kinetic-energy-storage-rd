from models.hybrid_hil_profile import p1_reference_profile, run_profile
from models.hybrid_power_buffer import DispatchConfig, HybridLimits


def limits():
    return HybridLimits(
        battery_discharge_w=120.0,
        battery_charge_w=80.0,
        flywheel_discharge_w=100.0,
        flywheel_charge_w=80.0,
        flywheel_soc_min=0.1,
        flywheel_soc_max=0.9,
    )


def test_reference_profile_is_fully_served_and_reduces_battery_peak():
    r = run_profile(
        p1_reference_profile(),
        dt_s=0.05,
        initial_soc=0.5,
        usable_flywheel_energy_j=31.0,
        limits=limits(),
        cfg=DispatchConfig(alpha=0.08, soc_target=0.5, soc_gain_w=20.0),
    )
    assert r.unmet_energy_j < 1e-9
    assert r.peak_reduction_fraction > 0.10
    assert 0.1 <= r.final_flywheel_soc <= 0.9


def test_soc_energy_accounting_respects_released_reserve():
    r = run_profile(
        [100.0] * 100,
        dt_s=0.1,
        initial_soc=0.11,
        usable_flywheel_energy_j=5.0,
        limits=limits(),
        cfg=DispatchConfig(alpha=0.05, soc_target=0.5, soc_gain_w=0.0),
    )
    assert r.final_flywheel_soc == 0.1
    assert r.battery_peak_w <= 120.0


def test_invalid_inputs_rejected():
    cfg = DispatchConfig()
    for dt_s, energy_j, soc in [(0.0, 10.0, 0.5), (0.1, 0.0, 0.5), (0.1, 10.0, 1.1)]:
        try:
            run_profile([1.0], dt_s, soc, energy_j, limits(), cfg)
            assert False
        except ValueError:
            pass
