# P1 Independent Overspeed Release

Status: desktop release for the existing low-energy P1 envelope only.

This subsystem exists to remove motoring permission independently of VESC commutation telemetry. It does not increase the operating envelope. P1 remains limited to 1500 RPM commanded, 1650 RPM overspeed trip, <=5 A battery discharge, <=1 A regenerative battery current, and the existing ~38 J maximum reference rotor energy.

## Sensor target

Use an independent optical interrupter or reflective optical sensor viewing a **12-feature encoder target** fixed to the rotor shaft or 48T pulley. The target must rotate 1:1 with the rotor shaft and must not use motor electrical commutation as its source.

Why 12 features:
- 250 RPM -> 50 pulses/s -> 20.000 ms period
- 1500 RPM -> 300 pulses/s -> 3.333 ms period
- 1650 RPM -> 330 pulses/s -> 3.030 ms period

This provides ample pulse density throughout the released commissioning ladder and keeps overspeed detection latency in the millisecond range while retaining the repository's 0.25 s stale-channel gate.

The encoder target may be a laser-cut/printed opaque disk, slotted flag, or high-contrast reflective ring, provided all 12 features are equally spaced and rigidly attached. It is instrumentation only; it must not materially change the rotor energy or balance. Recheck rotor runout/balance after installation.

## Required electrical behavior

The independent-speed path must have its own sensor input and supervisor processing. It may share the low-voltage instrumentation supply, but it must not derive rotor speed from the VESC.

Required fail-safe chain:

```text
independent optical sensor
        |
        v
independent supervisor input
        |
        +-- rpm >=1650 --------------------------+
        +-- pulse stale >0.25 s after motion ----+--> latch FAULT
        +-- >5% disagreement vs VESC telemetry --+
                                                   |
                                                   v
                                           remove PERMISSIVE
                                                   |
                                                   v
NC E-stop -- supervisor permissive -- K1 coil --> battery contactor
```

A latched fault commands zero torque and requests K1 OPEN. The physical NC E-stop remains able to drop K1 without software participation.

## Startup/stale-channel semantics

A stationary rotor produces no speed pulses. Therefore the stale-pulse gate must not make initial motion impossible.

Released behavior:
1. before motion is observed in the current commanded run, lack of pulses does not by itself trip the stale gate;
2. once valid independent motion has been observed, pulse age >0.25 s during a commanded run latches `independent_rpm_stale`;
3. the pre-run dry check must prove the sensor produces pulses by hand-turning the shaft;
4. any sensor dropout after motion is established is fail-closed.

This resolves the otherwise contradictory requirement of a 0.25 s stale timeout while starting from zero RPM.

## Calibration and acceptance

Before belt-enabled powered testing:
- hand-turn the shaft and verify exactly 12 pulses per revolution;
- compare independent RPM against a handheld tachometer or counted-revolution reference at low speed;
- verify `period_to_rpm()` mapping with `PULSES_PER_REV=12`;
- inject/simulate 1650 RPM or faster pulse timing and verify the supervisor latches a fault;
- verify 1649 RPM equivalent pulse timing does not trip the overspeed threshold;
- verify removing the sensor signal after motion has been observed produces a stale fault within 0.25 s;
- verify a latched fault cannot be cleared merely by the speed falling below threshold;
- verify fault handling requests K1 OPEN while the passive 22 ohm dump remains connected to the isolated controller-side bus.

For a 12-feature target, the exact overspeed boundary is:

```text
1650 RPM = 330.000 Hz = 3.030303 ms between pulses
```

The implementation must treat **RPM >=1650** as overspeed; rounding must not move the trip above 1650 RPM.

## Desktop executable gate

`overspeed_gate.py` is the repository reference implementation for pulse-period conversion, overspeed thresholding, stale-channel behavior, VESC disagreement, and fault latching.

Run:

```bash
python prototype/p1_single_rotor/overspeed_gate.py
pytest -q tests/test_p1_overspeed_gate.py
```

The model is not a substitute for the physical cut-power chain. It exists to prevent threshold/sign/timing drift between the released mechanical limits, supervisor logic, commissioning records, and eventual embedded implementation.
