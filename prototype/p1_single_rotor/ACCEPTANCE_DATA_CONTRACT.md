# P1 Acceptance Data Contract

Every physical run should produce a CSV with at least:

- time_s
- commanded_rpm
- measured_rpm
- bus_voltage_v
- bus_current_a
- vibration_g
- motor_temp_c
- controller_temp_c
- bearing_left_temp_c
- bearing_right_temp_c
- fault_state

## Sign convention

- positive bus current = electrical power entering the controller/rotor system
- negative bus current = regenerated electrical power returned to the DC bus

## Derived quantities

For every charge/discharge cycle compute:

- electrical charge energy, J
- electrical recovered energy, J
- bench round-trip efficiency
- rotor kinetic energy at start/end of each phase
- coast-down loss power estimate
- peak vibration
- peak temperature of each monitored component
- time to accelerate 300 -> 1500 RPM
- time to regenerate 1500 -> 300 RPM

`acceptance_analyzer.py` is the executable reference for energy sign convention, five-cycle repeatability, fault/witness-mark checks, and the released coefficient-of-variation limits.

## P1 decision threshold

P1 is considered a successful architecture demonstrator if:

1. five consecutive regenerative cycles complete without fault;
2. returned electrical energy is positive and repeatable;
3. recovered-energy coefficient of variation across the five cycles is <10%;
4. coast-down tests are repeatable within 10%;
5. no monotonic vibration growth occurs across the speed range;
6. no hub/shaft witness-mark movement is observed;
7. bearing, motor, and controller temperatures remain stable within their component ratings.

No minimum round-trip efficiency is imposed at P1 because atmospheric windage, commodity bearings, and the temporary drive train are intentionally not optimized.

## Physical-review boundary

Criteria 5 and 7 remain physical review gates. The repository does not yet contain evidence-backed universal numeric vibration or temperature thresholds for the as-built rig. The analyzer therefore defaults those gates to **not passed** unless the test operator explicitly records that the vibration-growth review and component-specific thermal review passed.

This prevents a clean numerical energy dataset from falsely authorizing acceptance when mechanical or thermal behavior has not been reviewed.
