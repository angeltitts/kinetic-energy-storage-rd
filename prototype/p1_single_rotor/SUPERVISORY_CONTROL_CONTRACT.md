# P1 Independent Supervisory Control Contract

## Purpose

Close the software gap between the released P1 mechanical/electrical design and powered commissioning. The VESC performs motor control, but P1 also requires an independent speed channel that can latch a fault without trusting motor commutation telemetry alone.

This contract does **not** change the released physical envelope:

- rotor command limit: 1500 RPM
- overspeed trip: 1650 RPM
- reference maximum energy at 1650 RPM: ~38 J
- atmospheric operation only
- full guard required

## Independent supervisor inputs

Minimum inputs:

1. independent rotor RPM sensor;
2. VESC-derived rotor RPM for cross-check only;
3. monotonic time;
4. commanded-run state.

The independent sensor should be physically separate from the VESC motor-position/commutation estimate.

## Latched fault conditions

The supervisor latches and requires explicit reset for:

- independent rotor RPM >= 1650 RPM;
- missing independent speed channel when a run is commanded;
- independent speed sample older than 0.25 s during a commanded run;
- >5% disagreement between independent RPM and VESC-derived rotor RPM during a commanded run;
- physically impossible negative RPM values in the current unidirectional P1 test configuration.

A latched software fault commands zero torque and requests DC-bus isolation. The physical emergency-stop/contactor remains independent and authoritative; software is not a substitute for the hard power cut-off.

## Belt and electrical-RPM mapping

Released pulley ratio:

- motor pulley: 15 teeth
- rotor-shaft pulley: 48 teeth
- motor:rotor speed ratio = 48 / 15 = 3.2

For the released 12N/14P motor, there are 7 pole pairs.

Therefore:

- 1500 rotor RPM -> 4800 motor RPM -> 33,600 ERPM
- 1650 rotor RPM -> 5280 motor RPM -> 36,960 ERPM

Both are below the documented 60,000 ERPM controller ceiling. This confirms the controller ERPM ceiling is not the P1 overspeed protection mechanism; the independent 1650 rotor-RPM trip remains required.

## Commissioning behavior

Before enabling motor torque:

1. verify the independent RPM channel updates at hand rotation;
2. verify VESC RPM and independent RPM have the same sign/scaling;
3. simulate a stale independent sensor and confirm the latch;
4. simulate >=1650 RPM in the supervisor input path without physically spinning the rotor to that speed and confirm the latch;
5. verify the latched state commands zero torque;
6. verify the physical E-stop removes controller power independently of software.

Only after those checks should the released 250/500/750/1000/1250/1500 RPM commissioning sequence begin.

## Source of executable truth

`supervisor.py` contains the executable conversion and fault logic. `tests/test_p1_supervisor.py` regression-locks the released limits and gear/ERPM mapping.
