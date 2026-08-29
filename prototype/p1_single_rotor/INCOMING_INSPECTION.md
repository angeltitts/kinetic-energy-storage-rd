# P1 Incoming Inspection Gate

Purpose: convert delivered-part and assembled-runout observations into a reproducible, fail-closed record before powered commissioning.

## Required measurements

Record these values from the actual purchased/fabricated parts:

- motor mounting bolt count
- motor bolt-circle diameter
- motor mounting-hole diameter
- motor center-clearance diameter
- shaft diameter
- bearing bore
- shaft-pulley runout
- assembled rotor radial runout at OD
- assembled rotor axial wobble at OD

Also record explicit inspection dispositions for:

- shaft/bearing fit acceptable
- pulley runout acceptable for the purchased component/installation

The gate deliberately does **not** invent numeric shaft-fit or pulley-runout tolerances that are absent from the released design. Those measurements must exist and an inspector must explicitly disposition them. The already released rotor limits remain quantitative and enforceable:

- rotor radial runout at OD <= 0.25 mm
- rotor axial wobble at OD <= 0.25 mm

## JSON record

Example only; replace every value with measurements from the actual hardware:

```json
{
  "motor_bolt_count": 4,
  "motor_bolt_circle_mm": 38.0,
  "motor_hole_diameter_mm": 4.0,
  "motor_center_clearance_mm": 12.0,
  "shaft_diameter_mm": 12.0,
  "bearing_bore_mm": 12.0,
  "pulley_runout_mm": 0.05,
  "rotor_radial_runout_mm": 0.12,
  "rotor_axial_wobble_mm": 0.10,
  "shaft_bearing_fit_ok": true,
  "pulley_runout_disposition_ok": true
}
```

Run:

```bash
python prototype/p1_single_rotor/incoming_inspection.py path/to/p1_incoming_inspection.json
```

Exit code 0 means the record is complete and satisfies the released rotor runout/wobble limit. Exit code 2 means powered commissioning remains blocked.

## Fabrication sequence implication

1. Receive motor, shaft, bearings, pulleys and machined rotor/hub.
2. Measure the motor face before drilling the adjustment plate.
3. Measure shaft and bearing bore and disposition their actual fit.
4. Assemble the shaft, bearings, hub and rotor.
5. Measure rotor radial runout and axial wobble at the OD.
6. Measure installed shaft-pulley runout and disposition it.
7. Save the JSON record with the test evidence.
8. Run the gate and retain the PASS output with the build record.
9. Only then proceed to the already released zero-speed electrical checks and staged low-speed commissioning.

This gate does not change any operating limit, material assumption, containment strategy or P1 architecture.
