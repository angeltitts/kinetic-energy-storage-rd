from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import solve_ivp

TORR_TO_PA = 133.322368

_GASES = {
    "helium": {"molar_mass": 4.002602e-3, "diameter_m": 2.6e-10, "viscosity_pa_s": 1.96e-5},
    "argon": {"molar_mass": 39.948e-3, "diameter_m": 3.4e-10, "viscosity_pa_s": 2.23e-5},
}


@dataclass
class InterRingShearModel:
    n_rings: int
    gap_m: float = 0.0005
    pressure_torr: float = 1e-3
    gas_species: str = "helium"
    temperature_k: float = 300.0
    mean_radius_m: float = 0.10
    axial_width_m: float = 0.02
    ring_mass_kg: float = 0.10

    def __post_init__(self) -> None:
        if self.n_rings < 2:
            raise ValueError("n_rings must be >= 2")
        if self.gap_m <= 0 or self.pressure_torr <= 0:
            raise ValueError("gap and pressure must be positive")
        key = self.gas_species.lower()
        if key not in _GASES:
            raise ValueError("gas_species must be Helium or Argon")
        self.gas_species = key
        self._last_result = None
        self._last_target_rpm = None

    def compute_knudsen_number(self, gap: float | None = None, pressure: float | None = None) -> dict:
        gap_m = self.gap_m if gap is None else gap
        pressure_torr = self.pressure_torr if pressure is None else pressure
        if gap_m <= 0 or pressure_torr <= 0:
            raise ValueError("gap and pressure must be positive")
        p = pressure_torr * TORR_TO_PA
        d = _GASES[self.gas_species]["diameter_m"]
        k_b = 1.380649e-23
        mean_free_path = k_b * self.temperature_k / (math.sqrt(2.0) * math.pi * d**2 * p)
        kn = mean_free_path / gap_m
        if kn < 0.01:
            regime = "continuum"
        elif kn < 0.1:
            regime = "slip"
        elif kn < 10.0:
            regime = "transition"
        else:
            regime = "free-molecular"
        return {"knudsen_number": kn, "mean_free_path_m": mean_free_path, "regime": regime}

    def _coupling_coefficient(self) -> float:
        gas = _GASES[self.gas_species]
        mu = gas["viscosity_pa_s"]
        area = 2.0 * math.pi * self.mean_radius_m * self.axial_width_m
        kn = self.compute_knudsen_number()["knudsen_number"]
        rarefaction = 1.0 / (1.0 + 2.0 * kn)
        return mu * area * self.mean_radius_m**2 / self.gap_m * rarefaction

    @property
    def ring_inertia_kg_m2(self) -> float:
        return self.ring_mass_kg * self.mean_radius_m**2

    def torque_transfer(self, inner_hub_rpm: float, time_array) -> dict:
        t = np.asarray(time_array, dtype=float)
        if t.ndim != 1 or len(t) < 2 or np.any(np.diff(t) <= 0):
            raise ValueError("time_array must be a strictly increasing 1D array")
        target = inner_hub_rpm * 2.0 * math.pi / 60.0
        c = self._coupling_coefficient()
        inertia = self.ring_inertia_kg_m2

        def rhs(_time, omega):
            dw = np.zeros(self.n_rings)
            for i in range(self.n_rings):
                torque = 0.0
                left_speed = target if i == 0 else omega[i - 1]
                torque += c * (left_speed - omega[i])
                if i < self.n_rings - 1:
                    torque += c * (omega[i + 1] - omega[i])
                dw[i] = torque / inertia
            return dw

        result = solve_ivp(
            rhs,
            (float(t[0]), float(t[-1])),
            np.zeros(self.n_rings),
            t_eval=t,
            rtol=1e-7,
            atol=1e-9,
        )
        if not result.success:
            raise RuntimeError(result.message)
        rpm = result.y * 60.0 / (2.0 * math.pi)
        self._last_result = {"time_s": result.t, "ring_rpm": rpm, "coupling_nms": c}
        self._last_target_rpm = inner_hub_rpm
        return self._last_result

    def get_acceleration_lag(self) -> float:
        if self._last_result is None or self._last_target_rpm is None:
            raise RuntimeError("Run torque_transfer() before get_acceleration_lag()")
        target = 0.95 * self._last_target_rpm
        outer = self._last_result["ring_rpm"][-1]
        idx = np.where(outer >= target)[0]
        return float(self._last_result["time_s"][idx[0]]) if len(idx) else math.inf
