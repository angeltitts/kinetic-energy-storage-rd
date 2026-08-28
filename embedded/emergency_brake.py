from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BrakeLimits:
    overspeed_rpm: float
    max_vibration_g: float
    max_bearing_temperature_k: float
    max_pressure_torr: float


class EmergencyBrakeController:
    """Software interlock model for low-energy prototype control.

    A physical prototype still requires an independent hardware power cut-off.
    """

    def __init__(self, limits: BrakeLimits) -> None:
        self.limits = limits
        self.latched = False
        self.reason = ""

    def evaluate(self, ring_rpm, vibration_g, bearing_temperature_k, pressure_torr) -> bool:
        if self.latched:
            return True
        if any(abs(float(rpm)) >= self.limits.overspeed_rpm for rpm in ring_rpm):
            self._trip("overspeed")
        elif vibration_g >= self.limits.max_vibration_g:
            self._trip("vibration")
        elif bearing_temperature_k >= self.limits.max_bearing_temperature_k:
            self._trip("bearing_temperature")
        elif pressure_torr >= self.limits.max_pressure_torr:
            self._trip("vacuum_loss")
        return self.latched

    def _trip(self, reason: str) -> None:
        self.latched = True
        self.reason = reason

    def reset(self) -> None:
        self.latched = False
        self.reason = ""
