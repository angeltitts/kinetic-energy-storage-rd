from __future__ import annotations

from dataclasses import dataclass


ROTOR_COMMAND_LIMIT_RPM = 1500.0
ROTOR_OVERSPEED_RPM = 1650.0
BATTERY_DISCHARGE_LIMIT_A = 5.0
BATTERY_REGEN_LIMIT_A = 1.0
REGEN_MIN_BUS_V = 24.0
REGEN_MAX_BUS_V = 28.0
MOTOR_POLES = 14
MOTOR_PULLEY_TEETH = 15
ROTOR_PULLEY_TEETH = 48


@dataclass(frozen=True)
class CommissioningConfig:
    rotor_command_rpm: float
    rotor_overspeed_rpm: float
    battery_discharge_limit_a: float
    battery_regen_limit_a: float
    regen_min_bus_v: float
    regen_max_bus_v: float
    motor_poles: int = MOTOR_POLES
    motor_pulley_teeth: int = MOTOR_PULLEY_TEETH
    rotor_pulley_teeth: int = ROTOR_PULLEY_TEETH


def motor_rpm_from_rotor_rpm(rotor_rpm: float, cfg: CommissioningConfig) -> float:
    return rotor_rpm * cfg.rotor_pulley_teeth / cfg.motor_pulley_teeth


def erpm_from_rotor_rpm(rotor_rpm: float, cfg: CommissioningConfig) -> float:
    pole_pairs = cfg.motor_poles / 2.0
    return motor_rpm_from_rotor_rpm(rotor_rpm, cfg) * pole_pairs


def validate_commissioning_config(cfg: CommissioningConfig) -> list[str]:
    errors: list[str] = []

    if cfg.rotor_command_rpm > ROTOR_COMMAND_LIMIT_RPM:
        errors.append("rotor command exceeds released 1500 RPM limit")
    if cfg.rotor_overspeed_rpm > ROTOR_OVERSPEED_RPM:
        errors.append("overspeed threshold exceeds released 1650 RPM limit")
    if cfg.rotor_overspeed_rpm <= cfg.rotor_command_rpm:
        errors.append("overspeed threshold must be above command limit")
    if cfg.battery_discharge_limit_a > BATTERY_DISCHARGE_LIMIT_A:
        errors.append("battery discharge current exceeds released 5 A limit")
    if cfg.battery_regen_limit_a > BATTERY_REGEN_LIMIT_A:
        errors.append("battery regenerative current exceeds released 1 A limit")
    if cfg.battery_discharge_limit_a <= 0:
        errors.append("battery discharge limit must be positive")
    if cfg.battery_regen_limit_a < 0:
        errors.append("battery regenerative limit cannot be negative")
    if cfg.regen_min_bus_v < REGEN_MIN_BUS_V:
        errors.append("regen minimum bus voltage is below released 24 V window")
    if cfg.regen_max_bus_v > REGEN_MAX_BUS_V:
        errors.append("regen maximum bus voltage is above released 28 V window")
    if cfg.regen_min_bus_v >= cfg.regen_max_bus_v:
        errors.append("regen voltage window is invalid")
    if cfg.motor_poles != MOTOR_POLES:
        errors.append("motor pole count does not match released 14-pole motor")
    if cfg.motor_pulley_teeth != MOTOR_PULLEY_TEETH or cfg.rotor_pulley_teeth != ROTOR_PULLEY_TEETH:
        errors.append("belt ratio does not match released 15T:48T drive")

    return errors


def released_config() -> CommissioningConfig:
    return CommissioningConfig(
        rotor_command_rpm=1500.0,
        rotor_overspeed_rpm=1650.0,
        battery_discharge_limit_a=5.0,
        battery_regen_limit_a=1.0,
        regen_min_bus_v=24.0,
        regen_max_bus_v=28.0,
    )


def released_erpm_limits() -> tuple[float, float]:
    cfg = released_config()
    return (
        erpm_from_rotor_rpm(cfg.rotor_command_rpm, cfg),
        erpm_from_rotor_rpm(cfg.rotor_overspeed_rpm, cfg),
    )


if __name__ == "__main__":
    cfg = released_config()
    errors = validate_commissioning_config(cfg)
    command_erpm, overspeed_erpm = released_erpm_limits()
    print(f"command limit: {cfg.rotor_command_rpm:.0f} rotor RPM = {command_erpm:.0f} ERPM")
    print(f"overspeed trip: {cfg.rotor_overspeed_rpm:.0f} rotor RPM = {overspeed_erpm:.0f} ERPM")
    if errors:
        raise SystemExit("INVALID P1 CONFIG: " + "; ".join(errors))
    print("P1 commissioning configuration: PASS")
