# P0 Bearing and Carrier Selection

## Decision for low-energy P0

Use three identical **4 inch square captive-ball lazy-Susan bearings** in the Triangle 4C / equivalent 4-inch pattern family, one per rotor level.

Verified procurement envelope from multiple current vendor listings:

- nominal outside size: 101.6 x 101.6 mm
- thickness: 7.93-7.94 mm
- center opening: 56.6-56.7 mm
- nominal mount-hole center spacing / PCD reported by vendors: about 55 mm (2.16 in)
- captive 1/4-inch balls
- nominal load rating: 300 lb / 136 kg for common 4-inch units
- supplied ungreased by some vendors

These ratings are far above P0's static rotor mass requirement; they are **not** treated as a high-speed rating. P0 remains a <=300 RPM commanded, <=330 RPM trip, low-energy atmospheric rig.

## Why this closes the carrier blocker

The previous mechanical envelope deliberately omitted the rotor-to-bearing connection. A 4-inch bearing fits beneath all three annular rotors: even the smallest Rotor C has 150 mm ID, leaving 24.2 mm radial clearance from a 101.6 mm square bearing envelope to the 150 mm rotor opening before carrier spokes are added.

The rotor itself does not bolt directly to the bearing. Each level uses a flat carrier spider:

1. bearing lower race fastens to the stationary support shelf;
2. bearing upper race fastens to a centered carrier plate/spider;
3. three or four radial carrier arms extend outward from the carrier center;
4. the clear polycarbonate annular rotor fastens to those arms at symmetric points;
5. the carrier and rotor rotate together; the shelf and lower race remain stationary.

This makes the support and torque path explicit and removes the misleading 'floating ring' geometry.

## Carrier fabrication rule

Do **not** pre-drill carrier or shelf bearing holes solely from nominal web dimensions. The inexpensive bearing family has vendor-to-vendor hole-pattern variation and some listings describe center spacing differently. Buy all three bearings from the same SKU/batch, measure the actual hole centers with calipers, and transfer-drill or match-drill the stationary shelf and carrier plates from the physical bearing.

Freeze the following geometry independent of vendor hole details:

- bearing maximum plan envelope: 102 x 102 mm
- bearing maximum stack thickness allowance: 8.5 mm
- carrier centered on rotor axis within 0.5 mm before final tightening
- carrier must not project into the neighboring rotor swept envelope
- rotor fasteners arranged symmetrically about the axis
- no adhesive-only structural attachment of rotor to carrier

## Procurement examples checked 2026-08-28

- Simply Bearings LAZY/4: 101.6 mm OD, 56.7 mm ID, 7.93 mm thick, 55 mm nominal PCD, 300 lb load.
- Craftparts LS0400: 101.6 x 101.6 mm, 7.94 mm high, 56.6 mm center opening, 54.86 mm mount-hole center-to-center, 300 lb load.
- Lee Valley 12K0102: 4-inch zinc-plated bearing, 300 lb nominal load, intended for 12-25 inch turntables.

Vendor load ratings are used only to show that static capacity is not the limiting P0 requirement. They do not validate balance, runout, friction, service life, or dynamic suitability at 300 RPM.

## Incoming inspection / acceptance before powered use

For each of the three purchased bearings:

1. confirm same SKU and physical pattern;
2. record actual outside dimensions, thickness, center opening, and hole centers;
3. hand-spin and reject obvious binding, ball-race damage, or gross wobble;
4. assemble bearing + carrier + rotor and measure edge runout by fixed pointer or dial indicator;
5. hand-spin through at least 20 revolutions and confirm no support/guard contact;
6. only then proceed to the existing low-speed single-rotor powered commissioning sequence.

The first physical build should record measured runout and coast-down time. Those measurements become calibration inputs for the digital mechanical model rather than assuming furniture-bearing friction/runout from catalog data.

## Remaining physical uncertainty

The selected bearing family removes the dimensional/procurement ambiguity but does **not** establish acceptable dynamic runout at P0 speed. That is now a measurable hardware property and should be treated as the next physical validation item.