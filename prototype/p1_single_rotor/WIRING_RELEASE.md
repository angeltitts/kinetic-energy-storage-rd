# P1 Wiring Release — Low-Energy Bench Prototype

Status: desktop engineering release for the existing P1 envelope only.

This wiring release does **not** increase the physical operating envelope. P1 remains limited to 1500 RPM commanded, 1650 RPM independent overspeed trip, <=5 A battery discharge, <=1 A regenerative battery current, and the existing ~38 J maximum reference rotor energy.

## Power topology

```text
24 V-class LiFePO4 battery
        |
      F1 10 A MAX
        |
   K1 main contactor
        |
        +---------------- P1 DC BUS + -------------------+
        |                                                |
        |                                                +-- Rdump 22 ohm >=100 W --+
        |                                                                         |
        +-- Ivesc independent current cross-check -- VESC/FSESC -- BLDC motor     |
        |                                                                         |
        +---------------- P1 DC BUS - --------------------------------------------+
        |
 battery negative
```

Critical topology rule: **Rdump is connected on the controller side of K1**, directly across the P1 DC bus. Opening K1 removes the battery source while leaving the dump load connected to the controller bus.

Recovered-energy measurement must be taken in the VESC branch (`Ivesc`), not at the battery terminals, because regenerated energy may divide between the battery and dump resistor.

## Emergency-stop / contactor control

Use a normally-closed, mechanically latching emergency-stop in the K1 coil/control circuit.

```text
control supply +
   |
 NC E-STOP
   |
 supervisor permissive / enable contact
   |
 K1 coil
   |
control return
```

The emergency-stop must be capable of dropping K1 **without software participation**. Software may remove the permissive, but software must not be required for the physical E-stop to open K1.

If the selected contactor requires a flyback device or coil suppression, install the suppression specified by the contactor manufacturer. Do not improvise a suppression network that materially delays contactor dropout.

## Required branch protection and isolation

- F1: 10 A maximum fuse in the battery-positive lead, as close to the battery source as practical.
- K1: DC-rated contactor/relay with voltage rating above the maximum charged battery voltage and continuous current rating above the imposed 5 A P1 battery limit.
- No fuse, switch, contactor, or software-controlled element is permitted between the P1 DC bus and the passive dump resistor during powered testing unless a later reviewed design explicitly replaces this topology.
- All exposed battery, bus, controller, and dump-resistor terminals must be finger-safe/covered before powered rotor operation.
- Battery remains physically outside the rotating guard.

## Controller / motor

- VESC-compatible controller: released Mini FSESC4.20-class hardware or approved equivalent.
- Motor: released sensored 5055 ~200 KV, 14-pole family or approved measured equivalent.
- Phase leads: controller U/V/W to motor phases per VESC motor-detection/commissioning procedure.
- Hall/sensor harness: use only the verified pinout for the delivered motor/controller pair. Do not assume wire colors are universal.
- Controller configuration must pass `vesc_config_gate.py` before powered rotor commissioning.

## Independent safety sensing

Independent rotor speed sensing is separate from VESC commutation telemetry.

Required channels:

```text
Independent RPM sensor  ---> supervisor RPM input
VESC telemetry          ---> supervisor comparison input
Bearing-frame accel.    ---> logger / vibration gate
Left bearing temp       ---> logger
Right bearing temp      ---> logger
Motor case temp         ---> logger
VESC heatsink temp      ---> logger
Dump resistor temp      ---> logger
VESC branch V/I         ---> acceptance logger
```

The independent RPM channel must remain capable of producing the 1650 RPM trip even if VESC speed telemetry is absent or incorrect.

## Safety-state truth table

| State | K1 battery contactor | VESC torque command | Dump resistor | Required result |
|---|---:|---:|---:|---|
| Power off | OPEN | 0 | connected to isolated bus | no energized controller bus |
| Precharge/bench config, rotor stationary | CLOSED only when authorized | 0 | connected | verify bus and dump thermal behavior |
| Normal motoring | CLOSED | commanded within gate | connected | <=1500 RPM |
| Controlled regeneration | CLOSED | negative torque within gate | connected | regen <=1 A battery limit, bus within released window |
| Software/sensor fault | OPEN requested | 0 | connected | source isolated, passive bus sink retained |
| Physical E-stop | OPEN independent of software | 0 / controller de-energizing | connected | battery source removed immediately by control chain |
| Overspeed >=1650 RPM | OPEN requested/latching | 0 | connected | no further motoring torque; source isolation request latched |

## Commissioning continuity checks — rotor stationary

Before installing/enabling the belt for powered rotation:

1. Battery disconnected: verify no short between DC bus rails.
2. Confirm F1 value is <=10 A.
3. Confirm K1 is in the battery-positive path, upstream of the P1 bus.
4. Confirm Rdump measures approximately 22 ohm across the controller-side bus and remains electrically connected when K1 is open.
5. Confirm E-stop physically removes K1 coil power without a software command.
6. Confirm controller power terminals have correct polarity.
7. Confirm independent RPM sensor powers/logs independently of VESC speed telemetry.
8. Confirm all temperature channels identify the correct physical sensor by warming each sensor individually by hand.
9. Confirm current-sensor polarity: motoring from battery to VESC is positive under the repository sign convention; regeneration toward the bus is negative at the VESC branch unless the logger contract defines the inverse explicitly.
10. Save the continuity/polarity record with the commissioning dataset.

## First energized stationary checks

With rotor mechanically prevented from rotating and motor torque disabled:

1. Close K1 and measure actual P1 bus voltage.
2. Verify controller boots without fault.
3. Verify dump resistor heating is consistent with its continuously connected topology and remains within the physical thermal acceptance check.
4. Open K1 via normal control and verify battery isolation.
5. Re-close K1, actuate the physical E-stop, and verify battery isolation independently of the supervisory software.
6. Do not proceed to powered rotation until these checks and the executable VESC/supervisor dry tests pass.

## Harness / routing constraints

- Keep phase leads and battery-current conductors physically separated from low-level RPM, accelerometer, temperature, and bus-monitor signal wiring where practical.
- Add strain relief at the controller, motor, battery, and moving/guard-adjacent harness transitions.
- No wiring may enter the rotor swept volume or belt/pulley swept volume.
- Route the independent RPM sensor harness so a belt or pulley failure cannot reasonably sever it before the sensor can register the event.
- Secure all harnesses before closing the guard.

## Build hold points

Powered rotor commissioning is blocked until all of the following are true:

- incoming inspection gate PASS;
- rotor radial runout <=0.25 mm;
- rotor axial wobble <=0.25 mm;
- guard installed and closed;
- wiring continuity/polarity record complete;
- physical E-stop/contact K1 drop test PASS;
- dump path resistance and mounting verified;
- VESC configuration gate PASS;
- independent overspeed supervisor dry-test PASS;
- logger channels verified.

Any deviation from this released topology that changes source isolation, dump-path availability, rotor speed, stored energy, containment, or current limits requires explicit engineering review before powered testing.
