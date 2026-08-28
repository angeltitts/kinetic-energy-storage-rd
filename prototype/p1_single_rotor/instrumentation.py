from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class Sample:
    time_s: float
    rpm: float
    bus_voltage_v: float
    bus_current_a: float
    vibration_g: float = 0.0


def kinetic_energy_j(inertia_kg_m2: float, rpm: float) -> float:
    omega = rpm * 2.0 * math.pi / 60.0
    return 0.5 * inertia_kg_m2 * omega**2


def integrate_bus_energy_j(samples: Iterable[Sample]) -> float:
    rows = list(samples)
    if len(rows) < 2:
        return 0.0
    total = 0.0
    for a, b in zip(rows[:-1], rows[1:]):
        dt = b.time_s - a.time_s
        if dt <= 0:
            raise ValueError("sample times must be strictly increasing")
        p0 = a.bus_voltage_v * a.bus_current_a
        p1 = b.bus_voltage_v * b.bus_current_a
        total += 0.5 * (p0 + p1) * dt
    return total


def round_trip_efficiency(
    charge_samples: Iterable[Sample],
    regen_samples: Iterable[Sample],
) -> float:
    e_in = integrate_bus_energy_j(charge_samples)
    e_regen_signed = integrate_bus_energy_j(regen_samples)
    if e_in <= 0:
        raise ValueError("charge energy must be positive")
    e_out = -e_regen_signed
    if e_out < 0:
        raise ValueError("regen samples must use negative bus current for returned power")
    return e_out / e_in


def coastdown_loss_power_w(
    inertia_kg_m2: float,
    rpm_start: float,
    rpm_end: float,
    duration_s: float,
) -> float:
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    delta_e = kinetic_energy_j(inertia_kg_m2, rpm_start) - kinetic_energy_j(
        inertia_kg_m2, rpm_end
    )
    return delta_e / duration_s
