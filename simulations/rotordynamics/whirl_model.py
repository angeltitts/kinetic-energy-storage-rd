from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class RotorDynamicsModel:
    outer_diameter_m: float
    radial_thickness_m: float
    material_density_kg_m3: float
    hoop_tensile_modulus_gpa: float
    k_r_n_m: float
    k_z_n_m: float
    axial_width_m: float | None = None
    clearance_m: float = 0.0005

    def __post_init__(self) -> None:
        if min(self.outer_diameter_m, self.radial_thickness_m, self.material_density_kg_m3,
               self.hoop_tensile_modulus_gpa, self.k_r_n_m, self.k_z_n_m) <= 0:
            raise ValueError("All physical inputs must be positive")
        if 2 * self.radial_thickness_m >= self.outer_diameter_m:
            raise ValueError("radial thickness is too large for the specified diameter")
        if self.axial_width_m is None:
            self.axial_width_m = self.radial_thickness_m

    @property
    def outer_radius_m(self) -> float:
        return self.outer_diameter_m / 2.0

    @property
    def inner_radius_m(self) -> float:
        return self.outer_radius_m - self.radial_thickness_m

    @property
    def mean_radius_m(self) -> float:
        return 0.5 * (self.outer_radius_m + self.inner_radius_m)

    @property
    def mass_kg(self) -> float:
        area = math.pi * (self.outer_radius_m**2 - self.inner_radius_m**2)
        return self.material_density_kg_m3 * area * float(self.axial_width_m)

    @property
    def polar_inertia_kg_m2(self) -> float:
        return 0.5 * self.mass_kg * (self.outer_radius_m**2 + self.inner_radius_m**2)

    def _base_natural_frequencies_hz(self) -> tuple[float, float]:
        fr = math.sqrt(self.k_r_n_m / self.mass_kg) / (2.0 * math.pi)
        fz = math.sqrt(self.k_z_n_m / self.mass_kg) / (2.0 * math.pi)
        return fr, fz

    def calculate_critical_speeds(self, rpm_max: float = 150000.0, points: int = 1501) -> dict:
        if rpm_max <= 0:
            raise ValueError("rpm_max must be positive")
        rpm = np.linspace(0.0, rpm_max, points)
        spin_hz = rpm / 60.0
        fr, fz = self._base_natural_frequencies_hz()
        gyro_coeff = 0.04
        forward_hz = np.sqrt(fr**2 + (gyro_coeff * spin_hz) ** 2) + gyro_coeff * spin_hz
        backward_hz = np.maximum(
            np.sqrt(fr**2 + (gyro_coeff * spin_hz) ** 2) - gyro_coeff * spin_hz,
            0.0,
        )
        axial_hz = np.full_like(rpm, fz)

        def crossings(freq_hz: np.ndarray) -> list[float]:
            delta = freq_hz - spin_hz
            idx = np.where(np.sign(delta[:-1]) != np.sign(delta[1:]))[0]
            out: list[float] = []
            for i in idx:
                x0, x1 = rpm[i], rpm[i + 1]
                y0, y1 = delta[i], delta[i + 1]
                if y1 == y0:
                    out.append(float(x0))
                else:
                    out.append(float(x0 - y0 * (x1 - x0) / (y1 - y0)))
            return out

        critical = {
            "forward_rpm": crossings(forward_hz),
            "backward_rpm": crossings(backward_hz),
            "axial_rpm": crossings(axial_hz),
        }
        return {
            "rpm": rpm,
            "spin_hz": spin_hz,
            "forward_hz": forward_hz,
            "backward_hz": backward_hz,
            "axial_hz": axial_hz,
            "critical_speeds": critical,
        }

    def plot_campbell_diagram(self, save_path: str | Path, rpm_max: float = 150000.0) -> Path:
        data = self.calculate_critical_speeds(rpm_max=rpm_max)
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(data["rpm"], data["forward_hz"], label="forward whirl")
        ax.plot(data["rpm"], data["backward_hz"], label="backward whirl")
        ax.plot(data["rpm"], data["axial_hz"], label="axial mode")
        ax.plot(data["rpm"], data["spin_hz"], linestyle="--", label="1x spin")
        ax.set_xlabel("Spin speed (RPM)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title("Reduced-order Campbell Diagram")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(path, dpi=180)
        plt.close(fig)
        return path

    def check_uncoupled_ring_expansion(self, rpm: float) -> dict:
        if rpm < 0:
            raise ValueError("rpm must be non-negative")
        omega = rpm * 2.0 * math.pi / 60.0
        r = self.mean_radius_m
        v = omega * r
        youngs_pa = self.hoop_tensile_modulus_gpa * 1e9
        delta_r = self.material_density_kg_m3 * v**2 * r / youngs_pa
        return {
            "rpm": rpm,
            "tip_speed_m_s": v,
            "radial_growth_m": delta_r,
            "clearance_m": self.clearance_m,
            "bridges_clearance": delta_r >= self.clearance_m,
            "clearance_margin_m": self.clearance_m - delta_r,
        }
