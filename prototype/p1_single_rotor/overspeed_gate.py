from dataclasses import dataclass

COMMAND_RPM_LIMIT = 1500.0
OVERSPEED_RPM = 1650.0
STALE_TIMEOUT_S = 0.25
MAX_RPM_DISAGREEMENT_FRAC = 0.05
PULSES_PER_REV = 12


def period_to_rpm(period_s: float, pulses_per_rev: int = PULSES_PER_REV) -> float:
    if period_s <= 0 or pulses_per_rev <= 0:
        raise ValueError("period_s and pulses_per_rev must be positive")
    return 60.0 / (period_s * pulses_per_rev)


def disagreement_fraction(independent_rpm: float, vesc_rpm: float) -> float:
    if independent_rpm < 0 or vesc_rpm < 0:
        raise ValueError("rpm must be nonnegative")
    denom = max(independent_rpm, vesc_rpm, 1.0)
    return abs(independent_rpm - vesc_rpm) / denom


@dataclass(frozen=True)
class SupervisorDecision:
    permit: bool
    latched_fault: bool
    reason: str


def evaluate(
    independent_rpm: float,
    pulse_age_s: float,
    vesc_rpm: float | None,
    prior_latched: bool = False,
    run_commanded: bool = True,
    motion_seen: bool = True,
) -> SupervisorDecision:
    """Fail-closed P1 independent-speed gate.

    `motion_seen` exists so a stationary rotor can be armed and begin to move without
    immediately tripping the stale-pulse gate. Once motion has been observed during a
    commanded run, a pulse age >250 ms latches the independent-sensor fault.
    """
    if independent_rpm < 0 or pulse_age_s < 0:
        raise ValueError("rpm and pulse_age_s must be nonnegative")
    if prior_latched:
        return SupervisorDecision(False, True, "latched_fault")
    if run_commanded and motion_seen and pulse_age_s > STALE_TIMEOUT_S:
        return SupervisorDecision(False, True, "independent_rpm_stale")
    if independent_rpm >= OVERSPEED_RPM:
        return SupervisorDecision(False, True, "overspeed")
    if run_commanded and vesc_rpm is not None:
        if disagreement_fraction(independent_rpm, vesc_rpm) > MAX_RPM_DISAGREEMENT_FRAC:
            return SupervisorDecision(False, True, "rpm_disagreement")
    return SupervisorDecision(True, False, "ok")


if __name__ == "__main__":
    for rpm in (250, 500, 750, 1000, 1250, 1500, 1650):
        period = 60.0 / (rpm * PULSES_PER_REV)
        print(f"{rpm:4d} rpm -> {period * 1000.0:7.3f} ms/pulse")
