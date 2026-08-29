from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class P1SupervisorLimits:
    command_rpm: float = 1500.0
    overspeed_rpm: float = 1650.0
    sensor_stale_s: float = 0.25
    rpm_disagreement_fraction: float = 0.05
    motor_to_rotor_ratio: float = 48.0 / 15.0
    motor_pole_pairs: int = 7


@dataclass(frozen=True)
class SupervisorSample:
    time_s: float
    independent_rpm: float
    vesc_rotor_rpm: float
    commanded_run: bool


class P1Supervisor:
    """Independent low-energy supervisory interlock model for P1.

    This model does not replace the physical E-stop/contactor. It represents the
    required independent RPM/fault logic that should command torque to zero and
    request DC-bus isolation when a fault is latched.
    """

    def __init__(self, limits: P1SupervisorLimits | None = None) -> None:
        self.limits = limits or P1SupervisorLimits()
        self.latched = False
        self.reason = ""
        self._last_independent_update_s: float | None = None

    def reset(self) -> None:
        self.latched = False
        self.reason = ""
        self._last_independent_update_s = None

    def update_independent_sensor_timestamp(self, time_s: float) -> None:
        self._last_independent_update_s = float(time_s)

    def evaluate(self, sample: SupervisorSample) -> bool:
        if self.latched:
            return True

        rpm = float(sample.independent_rpm)
        vesc_rpm = float(sample.vesc_rotor_rpm)

        if rpm < 0 or vesc_rpm < 0:
            return self._trip("invalid_negative_rpm")

        if rpm >= self.limits.overspeed_rpm:
            return self._trip("independent_overspeed")

        if sample.commanded_run:
            if self._last_independent_update_s is None:
                return self._trip("independent_sensor_missing")
            age = float(sample.time_s) - self._last_independent_update_s
            if age > self.limits.sensor_stale_s:
                return self._trip("independent_sensor_stale")

            denominator = max(rpm, vesc_rpm, 1.0)
            disagreement = abs(rpm - vesc_rpm) / denominator
            if disagreement > self.limits.rpm_disagreement_fraction:
                return self._trip("rpm_sensor_disagreement")

        return False

    def _trip(self, reason: str) -> bool:
        self.latched = True
        self.reason = reason
        return True


def rotor_rpm_to_motor_rpm(rotor_rpm: float, limits: P1SupervisorLimits | None = None) -> float:
    cfg = limits or P1SupervisorLimits()
    return float(rotor_rpm) * cfg.motor_to_rotor_ratio


def rotor_rpm_to_erpm(rotor_rpm: float, limits: P1SupervisorLimits | None = None) -> float:
    cfg = limits or P1SupervisorLimits()
    return rotor_rpm_to_motor_rpm(rotor_rpm, cfg) * cfg.motor_pole_pairs
