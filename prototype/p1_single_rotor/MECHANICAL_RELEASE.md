# P1 Mechanical Release v1.1

## Purpose

Freeze enough geometry to fabricate the low-energy single-rotor regenerative test article without inventing high-speed hardware.

## Released operating envelope

- command limit: 1500 RPM
- overspeed trip: 1650 RPM
- reference rotor stored energy: ~31.4 J at 1500 RPM
- no vacuum
- no composite rotor
- no destructive test
- full guard required for powered operation

## Base and layout

Base plate:
- 400 x 300 x 12 mm minimum
- aluminum preferred; steel acceptable

Shaft:
- 12 mm precision steel shaft
- nominal overall length: 260 mm
- rotor centered between bearings
- bearing center-to-center spacing: 170 mm nominal

Bearings:
- two 12 mm pillow-block bearings
- lower-risk commodity bearing class acceptable at this speed/energy
- incoming inspection must include free rotation, detectable play, and temperature during commissioning

## Rotor

6061-T6 aluminum disk:
- 200.0 mm OD
- 6.0 mm thickness
- concentric center feature/hub interface
- final mounted radial runout at OD <=0.25 mm
- final mounted axial wobble at OD <=0.25 mm

### Hub rule

Do not use a single radial set screw directly against the shaft as the sole rotor-retention method.

Use a concentric clamping-style hub or two-sided flange clamp that:
- centers the rotor on the shaft;
- positively captures the disk axially;
- has a mechanical retention feature against axial migration;
- can be witness-marked for inspection.

The exact commercial hub SKU may vary, but its rotor attachment must be symmetric.

## Guard

Clear polycarbonate:
- 6 mm minimum wall in the rotor plane
- 360-degree enclosure
- minimum rotor-to-guard radial clearance: 50 mm
- minimum rotor-to-guard axial clearance: 50 mm each side

Nominal internal guard envelope in CAD:
- 310 mm wide
- 220 mm deep
- 170 mm tall

The guard is not claimed to be certified burst containment. It is a low-energy debris/contact guard for the released ~38 J maximum reference condition.

## Motor coupling

Preferred:
- flexible coupling or 1:1 timing belt
- no rigid misaligned shaft coupling
- motor must not impose visible bearing preload

A belt drive is preferred if the chosen motor shaft cannot align closely with the 12 mm rotor shaft.

## Mechanical commissioning

Before motor power:
1. verify rotor/hub witness marks;
2. measure radial runout;
3. measure axial wobble;
4. hand-spin and confirm no rubbing;
5. verify shaft collars/retention;
6. install guard;
7. verify E-stop with controller at zero speed.

Stop testing if any witness mark moves, wobble grows, rubbing appears, or bearing temperature rises abnormally.
