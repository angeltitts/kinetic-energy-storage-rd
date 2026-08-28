# P0 Buildable Prototype — Three-Zone Differential Hoop Rig

## Goal

Build a real, low-energy benchtop prototype that demonstrates the defining DSHC architectural behavior:

- three concentric hoop-like rotors
- each rotor can spin at a different commanded speed
- each speed is measured independently
- coupling/disturbance between zones can be measured
- overspeed and vibration trigger a controlled shutdown

This prototype is **not** an energy-density demonstrator. It is a functional architecture demonstrator.

## Safety envelope

Hard limits for P0:

- maximum commanded speed: 300 RPM
- software overspeed trip: 330 RPM
- no vacuum
- no high-strength composite rotors
- no destructive testing
- transparent polycarbonate guard around the full rotating assembly
- physical emergency-stop switch must remove motor power directly

With the reference polycarbonate rotor dimensions below, total rotor kinetic energy at 300 RPM is approximately 1.6 J.

That keeps the experiment in a deliberately low stored-energy regime.

## Mechanical layout

Use three annular polycarbonate rotors stacked coaxially on separate bearing planes.

### Rotor dimensions

All rotors:
- material: polycarbonate
- thickness: 6 mm
- radial ring width: 15 mm
- central axis: common vertical axis

Rotor A:
- OD: 300 mm
- ID: 270 mm
- approximate mass: 97 g
- mean radius: 142.5 mm

Rotor B:
- OD: 240 mm
- ID: 210 mm
- approximate mass: 76 g
- mean radius: 112.5 mm

Rotor C:
- OD: 180 mm
- ID: 150 mm
- approximate mass: 56 g
- mean radius: 82.5 mm

Axial spacing between rotating planes:
- 15–20 mm minimum

### Support

For the first working prototype, do not use magnetic or HTS bearings.

Each rotor is supported by its own low-friction turntable/lazy-Susan bearing or equivalent low-speed bearing ring mounted to a stationary spacer plate.

The support structure should prioritize repeatability and independent rotation, not low mass.

### Drive

Each rotor has its own low-voltage DC gearmotor.

Recommended functional specification:
- 12 V brushed DC gearmotor
- no-load output speed in the 300–500 RPM range
- rubber or polyurethane friction drive wheel
- motor mounted tangentially to rotor OD
- spring-loaded motor bracket so drive-wheel pressure is repeatable

The friction drive avoids machining gear teeth into the rotor and makes experimentation simple.

## Electronics

Controller:
- Raspberry Pi Pico or Pico-compatible RP2040 board

Motor drivers:
- three independent brushed-DC H-bridge channels
- each rated comfortably above the chosen motor stall current

Sensors:
- one Hall-effect sensor per rotor
- one small magnet or magnetic index marker per rotor
- one 3-axis accelerometer on the stationary frame
- optional thermistor near each motor

Power:
- 12 V motor supply
- separate regulated logic supply if required
- emergency-stop switch physically interrupts the motor supply

## Instrumentation outputs

Log at minimum:
- timestamp
- target RPM for A/B/C
- measured RPM for A/B/C
- motor PWM command for A/B/C
- frame vibration magnitude
- overspeed/fault state

## Initial test sequence

### Test 1 — single-zone validation
Run one rotor at a time:
- 50 RPM
- 100 RPM
- 150 RPM
- 200 RPM

Verify:
- sensor stability
- speed-control stability
- no mechanical contact

### Test 2 — differential-speed operation
Command:
- A = 180 RPM
- B = 120 RPM
- C = 60 RPM

Hold for 60 s.

Then:
- A = 100 RPM
- B = 200 RPM
- C = 150 RPM

Hold for 60 s.

Pass condition:
- all three remain within ±5% of target
- no sustained contact
- no uncontrolled speed entrainment between rotors

### Test 3 — disturbance response
With all three rotating:
- lightly perturb one motor load through a controlled drive-pressure adjustment
- record response of all other rotor speeds and frame vibration

Goal:
quantify mechanical cross-coupling.

### Test 4 — controlled stop
Command zero RPM simultaneously.

Pass condition:
- all rotors stop without contact or oscillatory instability

### Test 5 — overspeed protection
Temporarily set one test target above 330 RPM in firmware simulation mode or by injecting a fake sensor value.

The software must:
- set all PWM outputs to zero
- latch a FAULT state
- require explicit reset

Do not physically overspeed the rotor to test the protection.

## Quantitative stored-energy check

For a thin annular rotor at low speed:

    E = 1/2 I omega^2

Using polycarbonate density near 1200 kg/m^3 and the dimensions above, approximate rotor energies at 300 RPM are:

- Rotor A: ~0.97 J
- Rotor B: ~0.48 J
- Rotor C: ~0.19 J

Total: ~1.63 J

## What constitutes a working P0 prototype

P0 is successful when a video/data log can demonstrate:

1. all three rotors spinning simultaneously;
2. all three at different commanded speeds;
3. closed-loop speed measurement and control;
4. stable operation for at least 10 minutes;
5. measured coupling/disturbance data;
6. a working hard motor-power E-stop;
7. a working software overspeed latch.

## What P0 does not prove

P0 does not validate:
- CNT material feasibility
- 500 Wh/kg performance
- multi-km/s rotordynamics
- vacuum losses
- HTS bearings
- high-energy containment

It validates the unusual multi-zone differential-hoop control architecture cheaply and safely.
