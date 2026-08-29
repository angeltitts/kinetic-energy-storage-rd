from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RotorEnvelope:
    name: str
    outer_diameter_mm: float
    inner_diameter_mm: float
    thickness_mm: float
    bottom_z_mm: float

    @property
    def top_z_mm(self) -> float:
        return self.bottom_z_mm + self.thickness_mm


BASE_X_MM = 450.0
BASE_Y_MM = 450.0
BASE_Z_MM = 10.0

MIN_SURFACE_GAP_MM = 18.0
NOMINAL_SURFACE_GAP_MM = 24.0
MIN_GUARD_RADIAL_CLEARANCE_MM = 25.0
GUARD_ID_MM = 380.0
GUARD_WALL_MM = 3.0

FIRST_ROTOR_Z_MM = BASE_Z_MM + 20.0
ROTOR_THICKNESS_MM = 6.0
LEVEL_PITCH_MM = ROTOR_THICKNESS_MM + NOMINAL_SURFACE_GAP_MM

ROTORS = (
    RotorEnvelope("A", 300.0, 270.0, ROTOR_THICKNESS_MM, FIRST_ROTOR_Z_MM),
    RotorEnvelope("B", 240.0, 210.0, ROTOR_THICKNESS_MM, FIRST_ROTOR_Z_MM + LEVEL_PITCH_MM),
    RotorEnvelope("C", 180.0, 150.0, ROTOR_THICKNESS_MM, FIRST_ROTOR_Z_MM + 2 * LEVEL_PITCH_MM),
)


def surface_gap_mm(lower: RotorEnvelope, upper: RotorEnvelope) -> float:
    return upper.bottom_z_mm - lower.top_z_mm


def guard_radial_clearance_mm(rotor: RotorEnvelope) -> float:
    return (GUARD_ID_MM - rotor.outer_diameter_mm) / 2.0


def validate_release_fit() -> dict[str, float | bool]:
    gaps = [surface_gap_mm(a, b) for a, b in zip(ROTORS, ROTORS[1:])]
    guard_clearances = [guard_radial_clearance_mm(r) for r in ROTORS]

    return {
        "base_matches_release": BASE_X_MM == 450.0 and BASE_Y_MM == 450.0 and BASE_Z_MM == 10.0,
        "minimum_surface_gap_mm": min(gaps),
        "surface_gap_pass": min(gaps) >= MIN_SURFACE_GAP_MM,
        "minimum_guard_radial_clearance_mm": min(guard_clearances),
        "guard_clearance_pass": min(guard_clearances) >= MIN_GUARD_RADIAL_CLEARANCE_MM,
        "guard_wall_pass": GUARD_WALL_MM >= 3.0,
    }


def legacy_cad_surface_gap_mm(level_pitch_mm: float = 22.0, rotor_thickness_mm: float = 6.0) -> float:
    """Return the clear rotor-surface gap in the pre-fix CAD model."""
    return level_pitch_mm - rotor_thickness_mm


if __name__ == "__main__":
    for key, value in validate_release_fit().items():
        print(f"{key}: {value}")
