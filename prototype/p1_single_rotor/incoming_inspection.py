from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

MAX_ROTOR_RUNOUT_MM = 0.25


@dataclass(frozen=True)
class IncomingInspection:
    motor_bolt_count: Optional[int]
    motor_bolt_circle_mm: Optional[float]
    motor_hole_diameter_mm: Optional[float]
    motor_center_clearance_mm: Optional[float]
    shaft_diameter_mm: Optional[float]
    bearing_bore_mm: Optional[float]
    pulley_runout_mm: Optional[float]
    rotor_radial_runout_mm: Optional[float]
    rotor_axial_wobble_mm: Optional[float]
    shaft_bearing_fit_ok: Optional[bool]
    pulley_runout_disposition_ok: Optional[bool]


def evaluate(record: IncomingInspection) -> tuple[bool, list[str]]:
    reasons: list[str] = []

    if not isinstance(record.motor_bolt_count, int) or record.motor_bolt_count < 3:
        reasons.append("motor_bolt_count missing/invalid")

    numeric = {
        "motor_bolt_circle_mm": record.motor_bolt_circle_mm,
        "motor_hole_diameter_mm": record.motor_hole_diameter_mm,
        "motor_center_clearance_mm": record.motor_center_clearance_mm,
        "shaft_diameter_mm": record.shaft_diameter_mm,
        "bearing_bore_mm": record.bearing_bore_mm,
        "pulley_runout_mm": record.pulley_runout_mm,
        "rotor_radial_runout_mm": record.rotor_radial_runout_mm,
        "rotor_axial_wobble_mm": record.rotor_axial_wobble_mm,
    }
    for name, value in numeric.items():
        if value is None or not isinstance(value, (int, float)) or value <= 0:
            reasons.append(f"{name} missing/invalid")

    # Only the released rotor runout/wobble limit is numerically enforced here.
    # Other purchased-part measurements are recorded and require an explicit
    # inspection disposition rather than inventing a new catalog tolerance.
    if isinstance(record.rotor_radial_runout_mm, (int, float)) and record.rotor_radial_runout_mm > MAX_ROTOR_RUNOUT_MM:
        reasons.append(f"rotor radial runout exceeds {MAX_ROTOR_RUNOUT_MM:.2f} mm")
    if isinstance(record.rotor_axial_wobble_mm, (int, float)) and record.rotor_axial_wobble_mm > MAX_ROTOR_RUNOUT_MM:
        reasons.append(f"rotor axial wobble exceeds {MAX_ROTOR_RUNOUT_MM:.2f} mm")

    if record.shaft_bearing_fit_ok is not True:
        reasons.append("shaft_bearing_fit_ok not confirmed")
    if record.pulley_runout_disposition_ok is not True:
        reasons.append("pulley_runout_disposition_ok not confirmed")

    return not reasons, reasons


def from_json(path: Path) -> IncomingInspection:
    return IncomingInspection(**json.loads(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(description="P1 incoming inspection gate")
    parser.add_argument("record", type=Path, help="inspection JSON record")
    args = parser.parse_args()

    record = from_json(args.record)
    passed, reasons = evaluate(record)
    print(json.dumps({"pass": passed, "reasons": reasons, "record": asdict(record)}, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
