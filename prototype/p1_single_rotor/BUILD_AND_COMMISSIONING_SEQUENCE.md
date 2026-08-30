# P1 Build and Commissioning Sequence

Status: released desktop build sequence for the existing low-energy P1 envelope only.

This sequence does not authorize any increase above 1500 RPM commanded, 1650 RPM independent overspeed trip, <=5 A battery discharge, <=1 A regenerative battery current, or the existing ~38 J maximum reference rotor energy.

## Rule

Do not skip hold points. A failed or incomplete hold point returns the build to the preceding safe state. Never demonstrate the overspeed trip by physically driving the rotor to 1650 RPM; test that trip by signal injection/dry simulation.

## Stage 0 — receive and inspect parts

1. Inventory every purchased and fabricated item against `BOM.md` and `PROCUREMENT_FREEZE.md`.
2. Record manufacturer/part number or the exact dimensional/electrical equivalent actually received.
3. Run the incoming inspection workflow in `INCOMING_INSPECTION.md` / `incoming_inspection.py`.
4. Measure the delivered motor face before drilling the adjustment plate. Feed measured bolt count, bolt-circle diameter, hole diameter, and center-clearance diameter to the released motor-interface checker/CAD.
5. Measure shaft diameter and both bearing bores; record the fit disposition.
6. Inspect the 15T motor pulley, 48T shaft pulley, 400 mm HTD-5M belt, shaft, bearings, rotor and hub parts for damage or obvious manufacturing defects.

**HOLD 0:** no assembly work proceeds with a failed incoming-inspection gate or an unresolved dimensional mismatch.

## Stage 1 — prepare stationary base

1. Use the released minimum 400 x 300 x 12 mm rigid base envelope.
2. Lay out the shaft axis, bearing locations, motor-adjustment-plate location and guard attachment footprint before drilling.
3. Keep the two bearing supports mutually aligned; do not use the rotor or belt to force misaligned bearings into position.
4. Install bearings finger-tight enough to permit final alignment adjustment.
5. Install the motor adjustment plate with the released adjustment range around the nominal 118.3 mm pulley center distance.

**HOLD 1:** shaft must pass through both bearings without binding before the rotor, pulley or belt is installed.

## Stage 2 — assemble shaft, hub and rotor

1. Clean the shaft, hub bores, rotor faces and clamp faces.
2. Assemble the released stack: rear hub flange | 6 mm rotor | front hub flange.
3. Install the six M5 rotor-capture screws in a star pattern with the released removable threadlocker requirement. Use fastener-manufacturer torque data; do not invent or exceed a torque value not released for the actual hardware.
4. Clamp both hub halves to the 12 mm shaft using their pinch features.
5. Position the rotor so all hub, bearing, pulley and future guard clearances are maintained.
6. Apply witness marks across both hub/shaft interfaces.
7. Measure rotor radial runout at the OD and axial wobble at the OD.

Acceptance: radial runout <=0.25 mm and axial wobble <=0.25 mm.

**HOLD 2:** if either runout limit is exceeded, stop and correct alignment/machining/fit. Do not compensate by increasing speed or tightening parts beyond their ratings.

## Stage 3 — install pulley transmission

1. Install the 48T / 12 mm-bore pulley on the rotor shaft and the 15T / 8 mm-bore pulley on the delivered motor shaft.
2. Align pulley faces with a straightedge or equivalent method before fitting the belt.
3. Install the 400 mm, 80-tooth, 15 mm-wide HTD-5M belt.
4. Use the motor plate to establish belt engagement without excessive pretension. No numeric belt tension is frozen until the delivered belt/pulley supplier data are available; use the component manufacturer's installation guidance.
5. Rotate the system by hand through multiple revolutions and confirm that the belt tracks consistently without flange climbing or visible cyclic tight spots.
6. Measure/disposition installed pulley runout per the incoming-inspection record.

**HOLD 3:** free hand rotation, stable belt tracking, no bearing bind, and no interference are mandatory.

## Stage 4 — install 360-degree guard

1. Install clear polycarbonate >=6 mm near the rotor plane. Acrylic is not an approved substitute.
2. Maintain >=50 mm radial clearance from the 200 mm rotor OD.
3. Enclose the rotor through 360 degrees and prevent normal hand access to the rotor, hub, pulley and belt swept volumes during powered operation.
4. Route all wiring outside rotor and belt swept volumes.
5. Verify guard hardware cannot loosen into a rotating element.

**HOLD 4:** no powered rotation is permitted with the guard removed, open, incomplete, or interfering.

## Stage 5 — wire the stationary electrical system

Follow `WIRING_RELEASE.md` exactly:

battery positive -> F1 <=10 A -> K1 contactor -> P1 DC bus -> VESC/controller -> motor

The 22 ohm, >=100 W dump resistor remains permanently connected across the controller-side P1 DC bus. The physical normally-closed latching E-stop must drop K1 without software participation.

Install and identify:
- VESC branch voltage/current cross-check;
- independent RPM sensor;
- bearing-frame accelerometer;
- left/right bearing temperature sensors;
- motor temperature sensor;
- VESC heatsink temperature sensor;
- dump-resistor temperature sensor.

Perform every stationary continuity and polarity check in `WIRING_RELEASE.md` before fitting/enabling a powered belt drive.

**HOLD 5:** E-stop/K1 isolation, fuse value, dump resistance/location, polarity, sensor identity and logging channels must all pass.

## Stage 6 — controller and independent-safety dry commissioning

1. Record actual VESC hardware and firmware revision.
2. Enter the released motor pole count, pulley ratio and current/speed limits.
3. Run `vesc_config_gate.py`; it must PASS.
4. Verify the independent 12-feature rotor-speed target/sensor path.
5. Dry-test the independent overspeed logic by injecting/simulating the 1650 RPM-equivalent pulse rate; verify the supervisor latches a source-isolation request.
6. Dry-test stale-sensor and RPM-disagreement faults.
7. Verify the physical E-stop remains authoritative even with supervisory software stopped.

**HOLD 6:** no rotor motoring until all controller and independent-safety dry checks pass.

## Stage 7 — first powered rotation

With guard closed and all personnel outside the rotor plane:

1. Begin at the lowest released motoring point, 250 RPM.
2. Confirm independent RPM and VESC-derived rotor RPM agree within the released supervisory tolerance.
3. Confirm no abnormal vibration growth, belt tracking issue, interference, witness-mark movement or unexpected temperature behavior.
4. Continue only through the released sequence: 250 / 500 / 750 / 1000 / 1250 / 1500 RPM, holding each point 30 s as specified by `RELEASE_SPEC.md`.
5. Any abnormal mechanical behavior, sensor fault, unexpected heating or safety-trip event ends the run and returns the system to a de-energized inspection state.

**HOLD 7:** P1-B motoring evidence must be saved before coast-down/regeneration testing.

## Stage 8 — coast-down characterization

1. Accelerate only to the released 1500 RPM command limit.
2. Remove drive torque without opening the passive dump topology.
3. Log independent RPM down to 300 RPM.
4. Repeat as required by the acceptance contract and retain the raw data.
5. Use repository analysis software for loss/repeatability reduction rather than hand-entered summary values.

## Stage 9 — controlled regeneration

1. Start with battery state suitable for charge acceptance; do not begin with a fully charged pack.
2. Confirm bus voltage is inside the released regeneration window and the passive dump path is connected.
3. Accelerate to no more than 1500 RPM.
4. Command controlled regenerative deceleration to 300 RPM while preserving the <=1 A battery-regeneration limit.
5. Log VESC-branch voltage/current, independent RPM and all physical-monitoring channels.
6. Recovered energy is calculated from the VESC branch, not battery-terminal current, because the passive dump intentionally shares regenerated energy.

## Stage 10 — repeatability and acceptance

1. Complete the released repeated charge/discharge/coast-down evidence set.
2. Inspect witness marks and all mechanical fasteners after testing.
3. Run `acceptance_analyzer.py` on the saved dataset.
4. Quantitative PASS is insufficient by itself: vibration-growth and component-specific thermal-stability reviews must be explicitly recorded as passed.
5. Archive the incoming-inspection record, VESC configuration record, wiring/continuity record, dry safety-test record, raw logs, analyzer output and photographs of the final guarded assembly as one P1 test article record.

## Stop conditions

Stop, isolate K1/battery power and inspect if any of the following occurs:
- independent overspeed/stale/disagreement trip;
- visible rotor/hub/pulley witness-mark motion;
- belt tracking loss or contact with guard;
- increasing vibration or new mechanical noise;
- unexpected component heating;
- bus voltage outside the released window during regeneration;
- current limit/configuration fault;
- guard damage or loss of enclosure integrity.

No response to a failed test may include increasing rotor speed, stored energy, current limits, or weakening containment.