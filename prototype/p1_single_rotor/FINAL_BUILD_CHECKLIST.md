# P1 Final Build Checklist

This checklist represents the point where software/design work stops and physical fabrication begins.

## Buy
- [ ] Flipsky 5055 200KV sensored BLDC motor
- [ ] Mini FSESC4.20
- [ ] Bioenno BLF-2410AS 24V 10Ah LiFePO4 battery (or approved equivalent)
- [ ] 22 ohm, >=100 W chassis-mount dump resistor
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

## Incoming inspection — required before powered commissioning
- [ ] measure actual motor mounting face before drilling the adjustment plate
- [ ] measure shaft diameter and bearing bore; explicitly disposition shaft/bearing fit
- [ ] measure installed shaft-pulley runout; explicitly disposition result
- [ ] verify assembled rotor radial runout at OD <=0.25 mm
- [ ] verify assembled rotor axial wobble at OD <=0.25 mm
- [ ] save measurements in the INCOMING_INSPECTION.md JSON format
- [ ] run `python prototype/p1_single_rotor/incoming_inspection.py <record.json>` and record PASS

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
- [ ] mount 22 ohm / >=100 W dump resistor thermally to metal base
- [ ] wire power, safety chain, dump path, sensing and logging exactly per WIRING_RELEASE.md
- [ ] place recovered-energy current measurement in VESC branch, excluding dump/battery branches
- [ ] verify all harnesses are strain-relieved and outside rotor/belt swept volumes

## Stationary wiring / safety release — belt disabled or rotor mechanically prevented from rotating
- [ ] verify F1 <=10 A in battery-positive lead
- [ ] verify K1 contactor is upstream of the P1 DC bus
- [ ] verify ~22 ohm dump remains across controller-side bus with K1 OPEN
- [ ] verify physical NC latching E-stop drops K1 without software participation
- [ ] verify controller DC polarity before energization
- [ ] verify independent RPM sensor operates independently of VESC telemetry
- [ ] identify every temperature channel against its physical sensor
- [ ] verify VESC-branch current polarity and save continuity/polarity record
- [ ] perform first energized stationary checks in WIRING_RELEASE.md before installing/enabling the belt

## VESC / supervisor initial limits
- [ ] run `python prototype/p1_single_rotor/vesc_config_gate.py` and record PASS
- [ ] save controller firmware/hardware revision and a screenshot/export/transcription of actual limits
- [ ] rotor command <=1500 RPM / <=33,600 ERPM equivalent with released 15:48 drive and 14-pole motor
- [ ] independent overspeed trip =1650 RPM / 36,960 ERPM equivalent
- [ ] independent RPM sample stale timeout =0.25 s during commanded run
- [ ] >5% independent-vs-VESC RPM disagreement latches a fault
- [ ] battery discharge current <=5 A
- [ ] regenerative battery current <=1 A with BLF-2410AS
- [ ] motor current limit conservative for first run
- [ ] battery not at full state-of-charge before regen test
- [ ] regen enabled only with measured DC bus in 24.0-28.0 V window

## Supervisory interlock dry checks — no powered rotor required
- [ ] hand-turn confirms independent RPM sensor updates and scaling
- [ ] simulated independent RPM >=1650 latches overspeed fault
- [ ] simulated stale independent RPM channel latches sensor fault
- [ ] simulated >5% sensor disagreement latches fault
- [ ] latched supervisor state commands zero torque / isolation request
- [ ] physical E-stop removes battery source independently of software while dump remains across controller bus

## Commission
- [ ] guard installed/closed before any powered rotor test
- [ ] verify dump resistance and secure thermal mounting before applying bus power
- [ ] verify dump temperature remains controlled during a stationary powered-bus hold
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
- [ ] measured returned energy at the VESC branch is positive
- [ ] recovered-energy coefficient of variation <10%
- [ ] coast-down repeatability <10%
- [ ] no monotonic vibration growth
- [ ] no witness-mark movement
- [ ] no abnormal bearing/motor/controller/dump-resistor heating

At this point P1 is a working flywheel energy-storage demonstrator and provides the data needed to decide P2.
