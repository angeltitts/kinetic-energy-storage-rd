# Open Questions

Rank questions by **impact × uncertainty**.

## Q-001 — System energy-density feasibility

**Phase 1 status: conditionally survives.**

At 20 GPa raw material strength, rho=1.5 g/cc, and SF=1.5, a 500 Wh/kg complete-system target requires approximately:

- <=0.60 total non-rotor mass / rotor mass if fatigue retention is ~65%
- ~8.64 GPa effective hoop stress
- ~2.40 km/s peripheral speed

See `results/phase1_feasibility.md`.

Priority: CRITICAL

## Q-002 — Complete non-rotor mass budget

Can containment + vacuum housing + stator + bearings + cryogenic hardware + electronics stay near or below ~0.60 kg per kg of rotor while providing a credible failure path?

This is now the highest-value kill question.

Priority: CRITICAL

## Q-003 — Progressive containment

What containment architecture can safely manage rotor failure without consuming the entire system-level specific-energy advantage?

Priority: CRITICAL

## Q-004 — Rotordynamics

Can a suspended hoop system remain stable at ~2.4 km/s peripheral speed for the 500 Wh/kg threshold case, and higher for future targets?

Priority: CRITICAL

## Q-005 — Fatigue and creep

Can a future macroscale ~20 GPa fiber architecture retain ~65% or more of raw tensile strength under the required cycle life and long-duration charged hold?

Priority: CRITICAL

## Q-006 — Differential-hoop stability

Can multiple concentric thin hoops operate at independent angular velocities with sufficiently low inter-ring coupling?

A low-energy P0 rig is defined in `prototype/P0_DIFFERENTIAL_HOOP_RIG.md`.

Priority: HIGH

## Q-007 — Rotor-zone actuation

What contactless actuation method delivers torque to a small number of independently rotating hoop zones with acceptable rotor heating and stator mass?

Priority: HIGH

## Q-008 — HTS bearing

Can the bearing provide sufficient force, stiffness, damping, and low AC loss while remaining outside the motor-generator ripple field?

Priority: HIGH