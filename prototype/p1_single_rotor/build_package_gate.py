from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P1_DIR = Path("prototype/p1_single_rotor")

REQUIRED_ARTIFACTS = (
    "README.md",
    "BOM.md",
    "PROCUREMENT_FREEZE.md",
    "RELEASE_SPEC.md",
    "MECHANICAL_RELEASE.md",
    "HUB_AND_ROTOR_DRAWING.md",
    "MOTOR_ADJUSTMENT_PLATE.md",
    "INCOMING_INSPECTION.md",
    "WIRING_RELEASE.md",
    "REGEN_DUMP_PATH.md",
    "VESC_COMMISSIONING_GATE.md",
    "INDEPENDENT_OVERSPEED_RELEASE.md",
    "SUPERVISORY_CONTROL_CONTRACT.md",
    "ACCEPTANCE_DATA_CONTRACT.md",
    "TEST_PLAN.md",
    "FINAL_BUILD_CHECKLIST.md",
    "BUILD_AND_COMMISSIONING_SEQUENCE.md",
    "incoming_inspection.py",
    "motor_interface.py",
    "vesc_config_gate.py",
    "overspeed_gate.py",
    "supervisor.py",
    "instrumentation.py",
    "acceptance_analyzer.py",
    "regen_dump.py",
    "cad/clamp_hub.scad",
    "cad/motor_adjustment_plate.scad",
    "cad/p1_assembly.scad",
)

RELEASE_INVARIANTS = {
    "RELEASE_SPEC.md": (
        "command speed limit: 1500 RPM",
        "overspeed trip: 1650 RPM",
        "current limit during first commissioning: 5 A",
    ),
    "WIRING_RELEASE.md": (
        "F1 10 A MAX",
        "Rdump 22 ohm >=100 W",
        "<=1 A regenerative battery current",
        "normally-closed, mechanically latching emergency-stop",
    ),
    "HUB_AND_ROTOR_DRAWING.md": (
        "OD: 200.00 +/-0.10",
        "thickness: 6.00 +/-0.10",
        "rotor radial runout at OD <=0.25",
        "rotor axial wobble at OD <=0.25",
    ),
    "BUILD_AND_COMMISSIONING_SEQUENCE.md": (
        "1500 RPM commanded",
        "1650 RPM independent overspeed trip",
        "Never demonstrate the overspeed trip by physically driving the rotor to 1650 RPM",
        "no powered rotation is permitted with the guard removed",
    ),
}


@dataclass(frozen=True)
class PackageGateResult:
    ok: bool
    missing_files: tuple[str, ...]
    missing_invariants: tuple[str, ...]


def inspect_build_package(repo_root: Path) -> PackageGateResult:
    p1 = repo_root / P1_DIR
    missing_files = tuple(
        rel for rel in REQUIRED_ARTIFACTS if not (p1 / rel).is_file()
    )

    missing_invariants: list[str] = []
    for rel, snippets in RELEASE_INVARIANTS.items():
        path = p1 / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                missing_invariants.append(f"{rel}: {snippet}")

    return PackageGateResult(
        ok=not missing_files and not missing_invariants,
        missing_files=missing_files,
        missing_invariants=tuple(missing_invariants),
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    result = inspect_build_package(repo_root)
    if result.ok:
        print("P1 BUILD PACKAGE: PASS")
        return 0

    print("P1 BUILD PACKAGE: FAIL")
    for rel in result.missing_files:
        print(f"MISSING FILE: {rel}")
    for item in result.missing_invariants:
        print(f"MISSING INVARIANT: {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
