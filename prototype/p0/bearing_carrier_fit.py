from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BearingEnvelope:
    outside_mm: float = 101.6
    thickness_mm: float = 7.94
    center_opening_mm: float = 56.7
    maximum_install_envelope_mm: float = 102.0
    maximum_stack_allowance_mm: float = 8.5


BEARING = BearingEnvelope()
ROTOR_IDS_MM = {"A": 270.0, "B": 210.0, "C": 150.0}


def radial_clearance_to_rotor_id_mm(rotor_id_mm: float, bearing_envelope_mm: float = BEARING.maximum_install_envelope_mm) -> float:
    if rotor_id_mm <= 0 or bearing_envelope_mm <= 0:
        raise ValueError("dimensions must be positive")
    return (rotor_id_mm - bearing_envelope_mm) / 2.0


def validate_bearing_carrier_envelope() -> dict[str, float | bool]:
    clearances = {name: radial_clearance_to_rotor_id_mm(rotor_id) for name, rotor_id in ROTOR_IDS_MM.items()}
    return {
        "minimum_radial_clearance_mm": min(clearances.values()),
        "smallest_rotor_clearance_mm": clearances["C"],
        "bearing_fits_all_rotor_ids": all(clearance > 0 for clearance in clearances.values()),
        "bearing_within_stack_allowance": BEARING.thickness_mm <= BEARING.maximum_stack_allowance_mm,
    }


if __name__ == "__main__":
    for key, value in validate_bearing_carrier_envelope().items():
        print(f"{key}: {value}")
