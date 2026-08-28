"""
Phase 2 non-rotor mass-budget gate.

Answers:
Given raw material strength, fatigue retention, safety factor, and target system
Wh/kg, how much total non-rotor mass is available? How much of that can be
allocated to containment after other subsystems are accounted for?

Screening only; not a validated mechanical design.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J_PER_WH = 3600.0


@dataclass(frozen=True)
class Case:
    raw_strength_gpa: float = 20.0
    density_kg_m3: float = 1500.0
    fatigue_retention: float = 0.65
    safety_factor: float = 1.5
    target_system_whkg: float = 500.0


def effective_stress_gpa(case: Case) -> float:
    return case.raw_strength_gpa * case.fatigue_retention / case.safety_factor


def rotor_whkg(case: Case) -> float:
    return effective_stress_gpa(case) * 1e9 / (2.0 * case.density_kg_m3 * J_PER_WH)


def max_total_nonrotor_ratio(case: Case) -> float:
    return rotor_whkg(case) / case.target_system_whkg - 1.0


def max_containment_ratio(case: Case, other_nonrotor_ratio: float) -> float:
    return max_total_nonrotor_ratio(case) - other_nonrotor_ratio


def build_rows() -> list[dict[str, float]]:
    rows = []
    for fatigue in [0.55, 0.60, 0.65, 0.70, 0.75]:
        case = Case(fatigue_retention=fatigue)
        total = max_total_nonrotor_ratio(case)
        for other in [0.25, 0.35, 0.45, 0.55]:
            rows.append(
                {
                    "fatigue_retention": fatigue,
                    "effective_stress_GPa": effective_stress_gpa(case),
                    "rotor_Wh_kg": rotor_whkg(case),
                    "max_total_nonrotor_ratio": total,
                    "assumed_other_nonrotor_ratio": other,
                    "max_containment_ratio": max_containment_ratio(case, other),
                    "feasible_before_containment_validation": max_containment_ratio(case, other) > 0,
                }
            )
    return rows


def main() -> None:
    rows = build_rows()
    out = ROOT / "results" / "phase2_mass_budget.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Phase 2 DSHC non-rotor mass-budget gate")
    for row in rows:
        if row["fatigue_retention"] == 0.65:
            print(
                f"fatigue={row['fatigue_retention']:.2f} "
                f"other={row['assumed_other_nonrotor_ratio']:.2f} "
                f"max_containment={row['max_containment_ratio']:.3f}"
            )


if __name__ == "__main__":
    main()
