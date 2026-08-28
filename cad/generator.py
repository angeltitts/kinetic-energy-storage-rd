from __future__ import annotations

from pathlib import Path
import cadquery as cq


def build_phase1_geometry(
    shaft_radius_mm: float = 25.0,
    hub_radius_mm: float = 75.0,
    hoop_wall_mm: float = 2.0,
    radial_gap_mm: float = 0.5,
    hoop_height_mm: float = 12.0,
    housing_clearance_mm: float = 0.5,
):
    if min(shaft_radius_mm, hub_radius_mm, hoop_wall_mm, radial_gap_mm, hoop_height_mm) <= 0:
        raise ValueError("all dimensions must be positive")
    if shaft_radius_mm >= hub_radius_mm:
        raise ValueError("shaft radius must be smaller than hub radius")

    parts: dict[str, cq.Workplane] = {}
    hub = cq.Workplane("XY").circle(hub_radius_mm).circle(shaft_radius_mm).extrude(hoop_height_mm)

    cryostat_r = 0.55 * hub_radius_mm
    cryostat = (
        cq.Workplane("XY")
        .circle(cryostat_r)
        .circle(shaft_radius_mm + 4.0)
        .extrude(hoop_height_mm * 0.7)
    )
    hub = hub.cut(cryostat.translate((0, 0, hoop_height_mm * 0.15)))
    parts["hub"] = hub

    inner_r = hub_radius_mm + radial_gap_mm
    for i in range(3):
        r0 = inner_r + i * (hoop_wall_mm + radial_gap_mm)
        r1 = r0 + hoop_wall_mm
        ring = cq.Workplane("XY").circle(r1).circle(r0).extrude(hoop_height_mm)
        parts[f"hoop_{i+1}"] = ring

    outer_rotor_r = inner_r + 3 * hoop_wall_mm + 2 * radial_gap_mm
    cavity_r = outer_rotor_r + housing_clearance_mm
    housing_outer_r = cavity_r + 4.0
    housing_h = hoop_height_mm + 12.0

    barrel = cq.Workplane("XY").circle(housing_outer_r).circle(cavity_r).extrude(housing_h)
    lower = cq.Workplane("XY").circle(housing_outer_r).extrude(2.0)
    upper = lower.translate((0, 0, housing_h - 2.0))
    parts["housing"] = barrel.union(lower).union(upper)
    parts["cryostat_pocket"] = cryostat
    return parts


def export_phase1(output_dir: str | Path) -> dict[str, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    parts = build_phase1_geometry()
    exported: dict[str, Path] = {}
    for name, solid in parts.items():
        step_path = output / f"{name}.step"
        stl_path = output / f"{name}.stl"
        cq.exporters.export(solid, str(step_path))
        cq.exporters.export(solid, str(stl_path))
        exported[f"{name}_step"] = step_path
        exported[f"{name}_stl"] = stl_path
    return exported


if __name__ == "__main__":
    export_phase1(Path(__file__).resolve().parents[1] / "docs" / "cad_exports")
