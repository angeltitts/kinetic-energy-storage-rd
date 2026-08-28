from __future__ import annotations

import csv
from pathlib import Path

from digital_twin import P0DigitalTwin


ROOT = Path(__file__).resolve().parents[2]


def run_virtual_commissioning() -> dict:
    twin = P0DigitalTwin()

    records = []
    sequence = [
        ((50, 0, 0), 5.0, "single_A_50"),
        ((100, 0, 0), 5.0, "single_A_100"),
        ((180, 120, 60), 60.0, "differential_1"),
        ((100, 200, 150), 60.0, "differential_2"),
    ]

    elapsed = 0.0
    dt = 0.01
    for targets, duration, label in sequence:
        for state in twin.run_constant(targets, duration, dt):
            elapsed += dt
            records.append(
                {
                    "time_s": elapsed,
                    "test": label,
                    "target_a": state["target_rpm"][0],
                    "rpm_a": state["measured_rpm"][0],
                    "target_b": state["target_rpm"][1],
                    "rpm_b": state["measured_rpm"][1],
                    "target_c": state["target_rpm"][2],
                    "rpm_c": state["measured_rpm"][2],
                    "fault": state["fault"],
                }
            )

    out = ROOT / "results" / "p0_virtual_commissioning.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    final = records[-1]
    errors = [
        abs(final["rpm_a"] - final["target_a"]) / final["target_a"],
        abs(final["rpm_b"] - final["target_b"]) / final["target_b"],
        abs(final["rpm_c"] - final["target_c"]) / final["target_c"],
    ]

    return {
        "output_csv": str(out),
        "total_rotor_energy_at_300rpm_j": twin.total_rotor_energy_at_300rpm_j,
        "final_tracking_error_fraction": errors,
        "passes_5pct_tracking": all(err <= 0.05 for err in errors),
        "fault": twin.fault_latched,
    }


if __name__ == "__main__":
    result = run_virtual_commissioning()
    for key, value in result.items():
        print(f"{key}: {value}")
