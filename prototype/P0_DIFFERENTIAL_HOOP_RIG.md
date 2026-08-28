# P0 Prototype Concept — Differential Hoop Dynamics Rig

## Purpose

P0 is **not** an energy-density demonstrator.

It is a deliberately low-energy laboratory rig intended to validate or falsify the architectural ideas that can be tested safely before any high-energy rotor work:

1. multiple concentric hoops can rotate at different angular velocities in one shared enclosure;
2. relative slip between hoops can remain dynamically stable;
3. speed can be measured and controlled independently;
4. coupling between adjacent hoops can be quantified;
5. vibration/whirl signatures can be detected early enough to command a controlled stop.

## Safety envelope

The P0 design must remain in a low stored-energy regime appropriate for guarded benchtop experimentation.

It must **not** attempt CNT-class stress, multi-km/s tip speeds, high-energy vacuum operation, or destructive burst testing.

Any later high-speed/high-energy rotor test requires qualified mechanical engineering review and a dedicated remote test facility.

## Mechanical concept

Use three lightweight concentric hoop rotors in a transparent guarded enclosure.

The first P0 version may use conventional low-risk support bearings rather than HTS suspension. This deliberately separates the core differential-hoop question from the bearing question.

Conceptual stack:

    stationary frame
        |
        +-- hoop zone A
        +-- hoop zone B
        +-- hoop zone C
        |
    optical speed sensing

Each hoop is mechanically independent and carries a simple optical index mark.

## Actuation

P0 should compare two low-energy actuation approaches:

### A. Independent conventional drive

Each hoop is driven independently through a laboratory-safe motor/bearing arrangement.

Purpose: establish control, differential-speed stability, instrumentation, and coupling measurements without requiring a new electromagnetic actuator on day one.

### B. Contactless electromagnetic demonstrator

After A is stable, replace one driven channel with a contactless stator/rotor coupling experiment.

Purpose: test the shaftless-I/O concept at low stored energy before it becomes part of the core architecture.

## Instrumentation

Minimum useful measurement set:

- independent optical RPM for each hoop
- enclosure vibration / accelerometer
- motor current and voltage
- hoop temperature
- commanded and measured acceleration/deceleration
- relative phase / slip rate where practical

## P0 success criteria

P0 succeeds if it demonstrates:

- three independently rotating concentric hoops
- stable commanded speed offsets between hoops
- repeatable acceleration and controlled stop
- measurable inter-ring coupling low enough that differential operation is practical
- vibration signatures that correlate with imbalance or speed transitions

P0 fails the architecture if:

- differential operation produces unavoidable unstable coupling even at low energy;
- adjacent hoops cannot be sufficiently isolated without excessive structural complexity;
- independent actuation/sensing overhead obviously scales worse than the projected system mass budget.

## Why this is the right first physical prototype

The 500 Wh/kg analytical gate requires future material and speed capabilities that do not exist in a manufacturable form today. Building a high-energy rotor first would therefore test too many unknowns simultaneously.

P0 isolates the unusual architectural claim—**differential concentric hoop operation**—using conventional, low-energy hardware.

If P0 fails, the high-energy DSHC concept can be rejected cheaply.

If P0 succeeds, P1 can focus on shaftless electromagnetic drive and magnetic suspension before any serious energy-density attempt.