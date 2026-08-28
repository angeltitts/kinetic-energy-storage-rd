"""
Phase 3 segmented-containment screening model.

Key idea:
If the rotor is divided into many mechanically independent hoops and common-mode
cascade can be prevented, the catcher may need to absorb only the energy of a
small number of failed hoops rather than the full rotor energy.

This model does NOT validate containment. It only quantifies the isolation
requirement implied by a target containment mass ratio and an assumed effective
specific energy absorption (SEA) for the catcher system.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J_PER_WH = 3600.0


@dataclass(frozen=True)
class ReferenceCase:
    rotor_specific_energy_whkg: float = 802.469135802469
    containment_mass_ratio: float = 0.15


def required_hoop_count(
    case: ReferenceCase,
    catcher_sea_mj_per_kg: float,
    simultaneous_failed_hoops: int = 1,
) -> int:
    if catcher_sea_mj_per_kg <= 0:
        raise ValueError("catcher_sea_mj_per_kg must be positive")
    if simultaneous_failed_hoops < 1:
        raise ValueError("simultaneous_failed_hoops must be >= 1")

    rotor_energy_mj_per_kg = case.rotor_specific_energy_whkg * J_PER_WH / 1e6
    # Total catcher capacity per kg of rotor:
    catcher_capacity_mj_per_kg_rotor = (
        case.containment_mass_ratio * catcher_sea_mj_per_kg
    )
    # k simultaneous hoops each contain k/N of total rotor energy.
    n = (
        rotor_energy_mj_per_kg * simultaneous_failed_hoops
        / catcher_capacity_mj_per_kg_rotor
    )
    return math.ceil(n)


def required_catcher_sea_mjkg(
    case: ReferenceCase,
    hoop_count: int,
    simultaneous_failed_hoops: int = 1,
) -> float:
    if hoop_count < 1:
        raise ValueError("hoop_count must be >= 1")
    rotor_energy_mj_per_kg = case.rotor_specific_energy_whkg * J_PER_WH / 1e6
    residual_fraction = simultaneous_failed_hoops / hoop_count
    return (
        rotor_energy_mj_per_kg
        * residual_fraction
        / case.containment_mass_ratio
    )


def main() -> None:
    case = ReferenceCase()
    rows = []
    for sea in [0.2, 0.5, 1.0, 2.0, 5.0]:
        for failed in [1, 2, 5, 10]:
            rows.append(
                {
                    "catcher_SEA_MJ_kg": sea,
                    "simultaneous_failed_hoops": failed,
                    "required_total_hoop_count": required_hoop_count(
                        case, sea, failed
                    ),
                }
            )

    out = ROOT / "results" / "phase3_segmented_containment.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Phase 3 segmented containment screen")
    for row in rows:
        if row["simultaneous_failed_hoops"] in (1, 5):
            print(row)


if __name__ == "__main__":
    main()
