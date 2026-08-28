"""
Phase 1 feasibility-envelope model for DSHC.

Purpose:
- answer what effective hoop stress is required to beat a complete-system target
- expose the direct coupling between non-rotor mass and required material performance
- keep rotor/cell/system comparisons explicit

This is a screening model, not a validated mechanical design.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J_PER_WH = 3600.0


@dataclass(frozen=True)
class Target:
    system_whkg: float = 500.0
    material_density_kg_m3: float = 1500.0
    raw_strength_gpa: float = 20.0
    safety_factor: float = 1.5


def rotor_whkg_from_effective_stress(effective_stress_gpa: float, density: float) -> float:
    return effective_stress_gpa * 1e9 / (2.0 * density * J_PER_WH)


def system_whkg(effective_stress_gpa: float, density: float, overhead_ratio: float) -> float:
    return rotor_whkg_from_effective_stress(effective_stress_gpa, density) / (1.0 + overhead_ratio)


def required_effective_stress_gpa(target_whkg: float, density: float, overhead_ratio: float) -> float:
    return target_whkg * (1.0 + overhead_ratio) * 2.0 * density * J_PER_WH / 1e9


def required_fatigue_retention(
    effective_stress_gpa: float, raw_strength_gpa: float, safety_factor: float
) -> float:
    return effective_stress_gpa * safety_factor / raw_strength_gpa


def tip_speed_m_s(effective_stress_gpa: float, density: float) -> float:
    return math.sqrt(effective_stress_gpa * 1e9 / density)


def rpm_for_radius(tip_speed: float, radius_m: float) -> float:
    return tip_speed / radius_m * 60.0 / (2.0 * math.pi)


def build_rows(target: Target) -> list[dict[str, float]]:
    rows = []
    for overhead in [0.40, 0.50, 0.60, 0.70, 0.80, 1.00, 1.45]:
        stress = required_effective_stress_gpa(
            target.system_whkg, target.material_density_kg_m3, overhead
        )
        tip = tip_speed_m_s(stress, target.material_density_kg_m3)
        fatigue = required_fatigue_retention(
            stress, target.raw_strength_gpa, target.safety_factor
        )
        rows.append(
            {
                "total_nonrotor_mass_per_rotor_mass": overhead,
                "required_effective_stress_GPa": stress,
                "required_fatigue_retention_at_SF1p5": fatigue,
                "required_tip_speed_m_s": tip,
                "rpm_at_0p5m": rpm_for_radius(tip, 0.5),
                "target_system_Wh_kg": target.system_whkg,
            }
        )
    return rows


def main() -> None:
    target = Target()
    rows = build_rows(target)
    out = ROOT / "results" / "phase1_500whkg_gate.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("500 Wh/kg complete-system gate, 20 GPa raw material, rho=1500 kg/m^3, SF=1.5")
    for row in rows:
        print(
            f"overhead={row['total_nonrotor_mass_per_rotor_mass']:.2f} "
            f"stress={row['required_effective_stress_GPa']:.2f} GPa "
            f"fatigue_retention={row['required_fatigue_retention_at_SF1p5']:.3f} "
            f"tip={row['required_tip_speed_m_s']:.0f} m/s "
            f"rpm@0.5m={row['rpm_at_0p5m']:.0f}"
        )


if __name__ == "__main__":
    main()
