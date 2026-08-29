# P1 Motor Adjustment Plate

Purpose: hold the selected Flipsky 5055-family motor and tension the 400 mm HTD 5M belt without inventing a motor-face drilling pattern.

## Plate geometry

- material: 6061-T6 or mild steel
- minimum plate: 120 x 90 x 6 mm
- 4 base slots: 7 mm wide x 22 mm long
- slot direction parallel to pulley centerline
- provide at least +/-10 mm center-distance adjustment around nominal 118.3 mm

## Motor-face rule — measured input is authoritative

The exact mounting pattern is **not released from an internet drawing**. Historical 5055-family references are not consistent enough to justify drilling before the purchased motor is inspected.

After the motor arrives, measure and record:

1. mounting-hole count;
2. mounting-hole center-to-center / bolt-circle diameter;
3. required clearance-hole diameter for the supplied fasteners;
4. central shaft/boss clearance diameter;
5. shaft diameter (expected 8 mm from current procurement evidence);
6. motor-body diameter and axial length.

Enter those values into `motor_interface.py` and `cad/motor_adjustment_plate.scad`. The plate may be drilled only if the executable geometry check leaves positive edge margin.

The SCAD defaults are placeholders for fit visualization, not purchasing truth and not machining authorization.

## Alignment acceptance

With the actual motor installed, the motor pulley and flywheel-shaft pulley must:

- have coplanar tooth faces within 0.5 mm;
- show no visible belt tracking against either flange;
- retain usable adjustment around the calculated ~118.3 mm nominal center distance;
- allow conservative belt tension without detectable bearing side preload.

## Belt

HTD 5M:
- width: 15 mm
- effective length: 400 mm
- 80 teeth

Do not over-tension. P1 torque and stored energy remain intentionally low.

## Evidence status

Current public procurement evidence supports a 5055-family body near 49-55 mm class, 8 mm shaft, 12N/14P, 200KV and 6-12S operation, but it does **not** remove the need to measure the mounting face of the purchased unit. This converts the remaining motor-plate uncertainty from a design blocker into a controlled incoming-inspection input.
