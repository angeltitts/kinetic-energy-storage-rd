from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


POLYCARBONATE_DENSITY_KG_M3 = 1200.0


@dataclass(frozen=True)
class AnnularRotor:
    outer_diameter_m: float
    inner_diameter_m: float
    thickness_m: float
    density_kg_m3: float = POLYCARBONATE_DENSITY_KG_M3

    @property
    def outer_radius_m(self) -> float:
        return self.outer_diameter_m / 2.0

    @property
    def inner_radius_m(self) -> float:
        return self.inner_diameter_m / 2.0

    @property
    def mass_kg(self) -> float:
        area = math.pi * (self.outer_radius_m**2 - self.inner_radius_m**2)
        return self.density_kg_m3 * area * self.thickness_m

    @property
    def inertia_kg_m2(self) -> float:
        return 0.5 * self.mass_kg * (
            self.outer_radius_m**2 + self.inner_radius_m**2
        )

    def kinetic_energy_j(self, rpm: float) -> float:
        omega = rpm * 2.0 * math.pi / 60.0
        return 0.5 * self.inertia_kg_m2 * omega**2


@dataclass
class PIController:
    kp: float = 0.08
    ki: float = 0.15
    integrator: float = 0.0

    def update(self, target_rad_s: float, measured_rad_s: float, dt: float) -> float:
        error = target_rad_s - measured_rad_s
        self.integrator += error * dt
        self.integrator = max(-20.0, min(20.0, self.integrator))
        return max(0.0, min(1.0, self.kp * error + self.ki * self.integrator))

    def reset(self) -> None:
        self.integrator = 0.0


@dataclass
class MotorChannel:
    rotor: AnnularRotor
    max_torque_nm: float = 0.05
    no_load_rpm: float = 450.0
    viscous_drag_nms: float = 2.0e-5
    omega_rad_s: float = 0.0
    controller: PIController | None = None

    def __post_init__(self) -> None:
        if self.controller is None:
            self.controller = PIController()

    def step(self, target_rpm: float, dt: float, enabled: bool = True) -> float:
        if not enabled:
            duty = 0.0
            self.controller.reset()
        else:
            target = target_rpm * 2.0 * math.pi / 60.0
            duty = self.controller.update(target, self.omega_rad_s, dt)

        no_load = self.no_load_rpm * 2.0 * math.pi / 60.0
        back_emf_factor = max(0.0, 1.0 - self.omega_rad_s / no_load)
        drive_torque = duty * self.max_torque_nm * back_emf_factor
        drag_torque = self.viscous_drag_nms * self.omega_rad_s
        net_torque = drive_torque - drag_torque

        self.omega_rad_s = max(
            0.0,
            self.omega_rad_s + (net_torque / self.rotor.inertia_kg_m2) * dt,
        )
        return duty

    @property
    def rpm(self) -> float:
        return self.omega_rad_s * 60.0 / (2.0 * math.pi)


class P0DigitalTwin:
    MAX_COMMAND_RPM = 300.0
    OVERSPEED_RPM = 330.0

    def __init__(self) -> None:
        self.channels = [
            MotorChannel(AnnularRotor(0.300, 0.270, 0.006)),
            MotorChannel(AnnularRotor(0.240, 0.210, 0.006)),
            MotorChannel(AnnularRotor(0.180, 0.150, 0.006)),
        ]
        self.fault_latched = False
        self.fault_reason = ""

    @property
    def rpms(self) -> list[float]:
        return [channel.rpm for channel in self.channels]

    @property
    def total_rotor_energy_at_300rpm_j(self) -> float:
        return sum(c.rotor.kinetic_energy_j(300.0) for c in self.channels)

    def reset_fault(self) -> None:
        if max(self.rpms) > 5.0:
            raise RuntimeError("rotors must be below 5 RPM before reset")
        self.fault_latched = False
        self.fault_reason = ""

    def force_fault(self, reason: str) -> None:
        self.fault_latched = True
        self.fault_reason = reason

    def step(
        self,
        targets_rpm: Iterable[float],
        dt: float,
        vibration_g: float = 0.0,
        vibration_trip_g: float = 1.0,
    ) -> dict:
        targets = [max(0.0, min(self.MAX_COMMAND_RPM, float(v))) for v in targets_rpm]
        if len(targets) != 3:
            raise ValueError("exactly three target RPM values are required")

        if max(self.rpms) > self.OVERSPEED_RPM:
            self.force_fault("overspeed")
        if vibration_g >= vibration_trip_g:
            self.force_fault("vibration")

        duties = [
            channel.step(target, dt, enabled=not self.fault_latched)
            for channel, target in zip(self.channels, targets)
        ]

        return {
            "target_rpm": targets,
            "measured_rpm": self.rpms,
            "duty": duties,
            "fault": self.fault_latched,
            "fault_reason": self.fault_reason,
        }

    def run_constant(
        self,
        targets_rpm: Iterable[float],
        duration_s: float,
        dt: float = 0.01,
    ) -> list[dict]:
        records = []
        steps = int(duration_s / dt)
        for index in range(steps):
            state = self.step(targets_rpm, dt)
            state["time_s"] = (index + 1) * dt
            records.append(state)
        return records
