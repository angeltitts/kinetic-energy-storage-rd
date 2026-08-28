from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p0"))

from mechanical_fit import (  # noqa: E402
    MIN_GUARD_RADIAL_CLEARANCE_MM,
    MIN_SURFACE_GAP_MM,
    ROTORS,
    guard_radial_clearance_mm,
    legacy_cad_surface_gap_mm,
    surface_gap_mm,
    validate_release_fit,
)


def test_current_release_fit_passes_all_frozen_clearances():
    result = validate_release_fit()
    assert result["base_matches_release"]
    assert result["surface_gap_pass"]
    assert result["guard_clearance_pass"]
    assert result["guard_wall_pass"]


def test_nominal_rotor_surface_gaps_exceed_release_minimum():
    gaps = [surface_gap_mm(a, b) for a, b in zip(ROTORS, ROTORS[1:])]
    assert gaps == [24.0, 24.0]
    assert min(gaps) >= MIN_SURFACE_GAP_MM


def test_guard_clearance_is_40_mm_at_largest_rotor():
    assert guard_radial_clearance_mm(ROTORS[0]) == 40.0
    assert guard_radial_clearance_mm(ROTORS[0]) >= MIN_GUARD_RADIAL_CLEARANCE_MM


def test_legacy_22_mm_pitch_fails_18_mm_surface_clearance():
    assert legacy_cad_surface_gap_mm() == 16.0
    assert legacy_cad_surface_gap_mm() < MIN_SURFACE_GAP_MM
