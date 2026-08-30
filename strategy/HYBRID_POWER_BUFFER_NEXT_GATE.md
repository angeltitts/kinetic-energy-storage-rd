# Next Development Gate — Hybrid Power Buffer

## Gate H1: prove the P1 flywheel hardware loop

Do not bypass the current P1 bench test.

Required physical evidence:
- stable motoring to 1500 RPM;
- repeatable coast-down;
- repeatable regeneration;
- measured E_in and E_out;
- vibration and temperature logs.

## Gate H2: hardware-in-the-loop hybrid control

After P1 passes, add a controllable DC load/source or emulated load profile.

Test profiles:
1. 0 -> 100% power step;
2. regenerative pulse;
3. repeating crane-like acceleration/deceleration cycle;
4. EV fast-charge ramp;
5. random industrial pulse train.

Measure:
- battery peak-power reduction;
- battery RMS-power reduction;
- flywheel energy throughput;
- curtailed regen;
- efficiency penalty.

## Gate H3: predictive battery-protection control

Only after H2 baseline data exists:
- add battery temperature and current limits;
- estimate battery stress/degradation cost;
- bias dispatch toward the flywheel during damaging high-C-rate events;
- compare against simple low-pass dispatch.

## Gate H4: mechanical loss reduction

P2/P3 work remains parallel:
- reduced-pressure rotor enclosure;
- non-cryogenic lower-loss bearing architecture;
- motor/inverter efficiency optimization.

## Success criterion

Advance toward a commercial prototype only if the hybrid system demonstrates a measurable customer-relevant gain such as:
- materially lower battery peak current;
- materially lower battery thermal rise;
- reduced required grid peak power;
- materially higher captured regenerative energy;
- or demonstrable battery-life extension in accelerated testing.
