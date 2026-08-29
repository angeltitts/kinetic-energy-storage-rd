# P0 Mechanical Fit Contract

This file makes the current Manufacturing Release v1 mechanical envelope executable and unambiguous.

## Frozen envelope

- base: 450 x 450 x 10 mm
- Rotor A: 300 OD / 270 ID / 6 mm
- Rotor B: 240 OD / 210 ID / 6 mm
- Rotor C: 180 OD / 150 ID / 6 mm
- minimum clear axial gap between rotating rotor surfaces: 18 mm
- nominal CAD clear axial gap: 24 mm
- nominal rotor pitch with 6 mm rotors: 30 mm
- guard wall: >=3 mm polycarbonate
- guard radial clearance from any moving rotor: >=25 mm
- nominal guard ID in the envelope model: 380 mm
- resulting clearance at the 300 mm rotor: 40 mm

`prototype/p0/mechanical_fit.py` is the executable source for these fit checks.

## Falsified legacy CAD geometry

The previous `p0_assembly.scad` used:

- a 440 x 440 x 12 mm base, inconsistent with the 450 x 450 x 10 mm Manufacturing Release;
- a 22 mm rotor level pitch with 6 mm-thick rotors.

Interpreting the release clearance as clear surface-to-surface spacing, that pitch yields only:

`22 - 6 = 16 mm`

which is below the 18 mm minimum. The corrected envelope uses a 30 mm pitch and therefore 24 mm clear surface gap.

## Remaining mechanical blocker

The exact **rotor-to-bearing carrier interface is not yet frozen**.

The repository currently permits a low-play turntable/lazy-Susan bearing or equivalent, but low-cost bearings have different outer diameters and bolt patterns. The annular rotors cannot be treated as self-supporting over an unspecified bearing opening. A real build therefore still requires one of the following before fabrication of the carrier plates:

1. select an exact bearing part number and design its adapter/carrier; or
2. define a universal slotted carrier geometry with enough adjustment for a bounded bearing-size family.

`p0_assembly.scad` deliberately models support/bearing envelopes rather than inventing a bolt pattern. Do not fabricate bearing carrier plates from the envelope model alone.

## Safety scope

This contract does not change the operating envelope. P0 remains limited to 300 RPM commanded speed, 330 RPM software overspeed trip, atmospheric operation, low-energy polycarbonate rotors, full guard, and no destructive testing.
