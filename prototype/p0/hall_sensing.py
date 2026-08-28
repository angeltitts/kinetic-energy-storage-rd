from __future__ import annotations

PULSES_PER_REV = 4
STALE_TIMEOUT_S = 0.75


def pulse_period_s(rpm: float, pulses_per_rev: int = PULSES_PER_REV) -> float:
    """Return seconds between Hall pulses for constant rotor speed."""
    if rpm <= 0:
        raise ValueError("rpm must be positive")
    if pulses_per_rev <= 0:
        raise ValueError("pulses_per_rev must be positive")
    return 60.0 / (rpm * pulses_per_rev)


def rpm_from_period_s(period_s: float, pulses_per_rev: int = PULSES_PER_REV) -> float:
    """Mirror the firmware's period-to-RPM conversion."""
    if period_s <= 0:
        raise ValueError("period_s must be positive")
    if pulses_per_rev <= 0:
        raise ValueError("pulses_per_rev must be positive")
    return 60.0 / (period_s * pulses_per_rev)


def is_stale(age_since_last_pulse_s: float, timeout_s: float = STALE_TIMEOUT_S) -> bool:
    if age_since_last_pulse_s < 0:
        raise ValueError("pulse age cannot be negative")
    return age_since_last_pulse_s > timeout_s
