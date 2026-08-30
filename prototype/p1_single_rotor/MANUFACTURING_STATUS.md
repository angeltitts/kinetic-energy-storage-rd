# P1 Manufacturing Status

## Status: DESKTOP BUILD PACKAGE COMPLETE — READY TO BUY, MACHINE, ASSEMBLE, AND TEST

The low-energy P1 single-rotor build package now has a controlled assembly/commissioning sequence and an executable package-completeness gate. The remaining evidence required for P1 acceptance is physical: delivered-part measurements, fabricated-part inspection, assembly alignment/runout, guarded bench operation, temperatures/vibration, coast-down, regeneration and repeatability logs.

Frozen desktop package:
- patent-conscious single-rotor commercial track and battery-protection hybrid power-buffer architecture
- rotor material and dimensions
- shaft size
- bearing class and geometry
- motor/controller class and selected products/equivalent rules
- belt pitch, tooth counts, width, length, ratio and nominal center distance
- DC-bus topology and commissioning current limits
- hub design and machining dimensions
- motor adjustment plate and measured-input drilling interface
- guard material/thickness/clearance requirements
- fuse / NC E-stop / K1 contactor / passive dump topology
- VESC configuration gate
- independent 12-feature overspeed sensing and dry-test contract
- instrumentation channels and acceptance data schema
- HIL hybrid-buffer load-profile model
- acceptance/data-reduction software
- staged build and commissioning sequence with explicit hold points
- final build checklist
- executable `build_package_gate.py` that fails closed if required build artifacts or core released safety invariants are removed

Released physical envelope remains unchanged:
- command speed <=1500 RPM
- independent overspeed trip at >=1650 RPM
- existing ~38 J maximum reference rotor energy
- battery discharge <=5 A during P1 commissioning
- regenerative battery current <=1 A
- F1 <=10 A
- 22 ohm / >=100 W passive dump retained across the controller-side bus
- rotor radial runout <=0.25 mm
- rotor axial wobble <=0.25 mm
- no powered rotor operation without the complete guard

Requires physical incoming-part/fabrication verification:
- measure the delivered motor face and enter bolt count, bolt circle, hole diameter and center clearance into the released motor-interface checker/CAD before drilling
- measure actual shaft diameter and bearing bores and disposition the fit
- verify delivered pulley/belt dimensions and installed pulley runout
- verify fabricated rotor/hub dimensions and material records
- verify assembled rotor radial runout and axial wobble at OD are each <=0.25 mm
- retain a passing `incoming_inspection.py` record before powered commissioning
- verify actual battery state-of-charge and regenerative charge acceptance behavior
- verify dump-resistor thermal mounting with the delivered part

Requires physical test evidence before P1 can pass:
- guarded motoring through the released 250 / 500 / 750 / 1000 / 1250 / 1500 RPM ladder
- vibration trend through the released speed range
- motor/controller/bearing/dump temperatures against actual component limits
- coast-down logs
- controlled regenerative-energy logs
- repeated recovered-energy/coast-down evidence required by the acceptance contract
- witness-mark stability
- explicit physical review of vibration growth and thermal stability

Do not physically drive to the 1650 RPM overspeed threshold to prove the trip. The overspeed path is commissioned by signal injection/dry simulation before powered rotor testing.

The next required engineering evidence is therefore only:
1. procurement and incoming inspection;
2. rotor/hub machining and dimensional inspection;
3. guarded assembly alignment/runout measurements;
4. stationary electrical/safety commissioning;
5. guarded powered motoring, coast-down and regenerative bench measurements.

Any proposed increase in rotor speed, stored energy, current limits, or reduction in guarding/containment remains outside this release and requires qualified mechanical/safety review.