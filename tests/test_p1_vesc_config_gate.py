import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from vesc_config_gate import (
    CommissioningConfig,
    released_config,
    released_erpm_limits,
    validate_commissioning_config,
)


def test_released_config_passes():
    assert validate_commissioning_config(released_config()) == []


def test_released_erpm_mapping():
    command_erpm, overspeed_erpm = released_erpm_limits()
    assert math.isclose(command_erpm, 33600.0, rel_tol=1e-12)
    assert math.isclose(overspeed_erpm, 36960.0, rel_tol=1e-12)


def test_rejects_speed_increase():
    cfg = CommissioningConfig(1501, 1650, 5, 1, 24, 28)
    assert any("1500 RPM" in e for e in validate_commissioning_config(cfg))


def test_rejects_regen_current_increase():
    cfg = CommissioningConfig(1500, 1650, 5, 1.01, 24, 28)
    assert any("1 A" in e for e in validate_commissioning_config(cfg))


def test_rejects_discharge_current_increase():
    cfg = CommissioningConfig(1500, 1650, 5.01, 1, 24, 28)
    assert any("5 A" in e for e in validate_commissioning_config(cfg))


def test_rejects_regen_voltage_window_expansion():
    cfg = CommissioningConfig(1500, 1650, 5, 1, 23.9, 28.1)
    errors = validate_commissioning_config(cfg)
    assert any("24 V" in e for e in errors)
    assert any("28 V" in e for e in errors)


def test_rejects_wrong_drive_ratio_or_motor_poles():
    cfg = CommissioningConfig(1500, 1650, 5, 1, 24, 28, motor_poles=12, motor_pulley_teeth=16)
    errors = validate_commissioning_config(cfg)
    assert any("14-pole" in e for e in errors)
    assert any("15T:48T" in e for e in errors)
