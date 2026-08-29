# P0 Manufacturing Release v1.0

Status: READY FOR LOW-ENERGY FABRICATION

Purpose: build the first physical architecture demonstrator for three independently controlled concentric hoop zones.

## Hard limits
- max commanded speed: 300 RPM
- overspeed trip: 330 RPM
- no vacuum
- no CNT/composite high-speed rotors
- no destructive testing
- transparent full guard required
- hard E-stop must remove motor power independently of firmware

## Mechanical release
Base:
- 450 x 450 x 10 mm aluminum or rigid HDPE plate

Rotors, clear polycarbonate:
- A: 300 OD / 270 ID / 6 mm
- B: 240 OD / 210 ID / 6 mm
- C: 180 OD / 150 ID / 6 mm

Rotor planes:
- minimum 18 mm axial spacing
- each rotor on its own low-play turntable bearing/support plane
- target radial runout after assembly: <= 0.5 mm at OD
- target axial wobble at OD: <= 0.75 mm

Guard:
- clear polycarbonate, minimum 3 mm wall
- full 360-degree enclosure
- minimum 25 mm clearance from any moving part

## Drive release
Per rotor:
- 12 V brushed DC gearmotor
- target no-load output: 300-500 RPM
- stall current <= 2.5 A
- 20-35 mm polyurethane/rubber friction wheel
- adjustable spring-loaded/slotted motor bracket

Motor drivers:
- 3 x PWM+DIR brushed DC drivers, 12 V capable, >= 3 A peak
- recommended interface class: MAX14870 carrier or equivalent

Controller:
- Raspberry Pi Pico / RP2040

Sensors:
- 3 digital Hall sensors
- 4 equally spaced retained magnets/index markers per rotor (12 total)
- 1 3-axis accelerometer on stationary frame

### Hall sensing geometry
The acceptance plan includes 50 RPM and a 60 RPM rotor in the 180/120/60 operating point. One pulse/revolution is too sparse for the control loop: 50 RPM produces one pulse every 1.20 s. The release therefore uses four equally spaced index magnets per rotor, giving pulse periods of 0.30 s at 50 RPM, 0.25 s at 60 RPM, 0.15 s at 100 RPM, and 0.05 s at 300 RPM. Firmware converts pulse period using `PULSES_PER_REV = 4` and marks speed stale after 0.75 s without a pulse.

Install all four magnets at equal 90-degree spacing and with equivalent radial position/retention so the sensing hardware does not introduce avoidable imbalance.

## Power
- 12 V, 5 A regulated DC supply
- 5 A inline fuse
- normally-closed latching mushroom E-stop in motor power path
- logic may remain USB-powered for logging after E-stop

## Acceptance
A working prototype must:
1. hand-spin freely with no contact;
2. verify four clean Hall pulses per mechanical revolution on each rotor by hand;
3. run each rotor independently at 50/100/150/200 RPM;
4. run A/B/C = 180/120/60 RPM for 60 s;
5. run A/B/C = 100/200/150 RPM for 60 s;
6. complete a 10-minute 180/120/60 RPM run;
7. hold each settled RPM within ±5%;
8. show no sustained rubbing/contact;
9. hard E-stop removes motor power;
10. software fault latch works via simulated overspeed;
11. produce CSV telemetry.

## Build sequence
P0-A mechanical dummy -> P0-B single powered zone -> P0-C three powered zones -> P0-D 10-minute acceptance run.
