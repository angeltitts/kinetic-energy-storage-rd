# P1 Final Build Checklist

This checklist represents the point where software/design work stops and physical fabrication begins.

## Buy
- [ ] Flipsky 5055 200KV sensored BLDC motor
- [ ] Mini FSESC4.20
- [ ] Bioenno BLF-2410AS 24V 10Ah LiFePO4 battery (or approved equivalent)
- [ ] 2 x KP001 12 mm pillow blocks
- [ ] 12 mm x 260 mm precision shaft
- [ ] 15T HTD5M x 15 mm pulley, 8 mm bore
- [ ] 48T HTD5M x 15 mm pulley, 12 mm bore
- [ ] 400-5M-15 timing belt, 80T
- [ ] 6 mm clear polycarbonate guard material
- [ ] E-stop, contactor/relay, 10 A fuse
- [ ] independent RPM sensor
- [ ] accelerometer
- [ ] temperature sensors
- [ ] wiring, terminals, covered connectors

## Machine
- [ ] 200 x 6 mm 6061-T6 rotor per HUB_AND_ROTOR_DRAWING.md
- [ ] front clamp flange
- [ ] rear clamp flange
- [ ] motor adjustment plate
- [ ] base plate holes after physical bearing/motor parts are in hand

## Bench assembly
- [ ] mount pillow blocks loosely
- [ ] install shaft
- [ ] align bearings before final tightening
- [ ] assemble two-flange hub and rotor
- [ ] verify runout/wobble <=0.25 mm
- [ ] mount 48T pulley
- [ ] mount motor/15T pulley
- [ ] install belt and align pulley faces
- [ ] install guard
- [ ] install independent RPM/vibration/temp sensing
- [ ] wire battery -> fuse -> E-stop/contactor -> VESC
- [ ] verify E-stop at zero speed

## VESC initial limits
- [ ] rotor command <=1500 RPM
- [ ] overspeed trip 1650 RPM in independent supervisory logic
- [ ] battery discharge current <=5 A
- [ ] regenerative battery current <=1 A with BLF-2410AS
- [ ] motor current limit conservative for first run
- [ ] battery not at full state-of-charge before regen test

## Commission
- [ ] 250 RPM / 30 s
- [ ] 500 RPM / 30 s
- [ ] 750 RPM / 30 s
- [ ] 1000 RPM / 30 s
- [ ] 1250 RPM / 30 s
- [ ] 1500 RPM / 30 s
- [ ] coast-down test x5
- [ ] regen test x5
- [ ] 20-cycle durability sequence

## Prototype is working when
- [ ] five consecutive regenerative cycles complete without fault
- [ ] measured returned energy is positive
- [ ] recovered-energy coefficient of variation <10%
- [ ] coast-down repeatability <10%
- [ ] no monotonic vibration growth
- [ ] no witness-mark movement
- [ ] no abnormal bearing/motor/controller heating

At this point P1 is a working flywheel energy-storage demonstrator and provides the data needed to decide P2.
