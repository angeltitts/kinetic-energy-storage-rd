# Research Note — What Tokamak Toroidal Dynamics Can (and Cannot) Contribute

## Purpose

This note evaluates whether physics mechanisms used in modern tokamak research can materially improve the kinetic-energy-storage project.

The answer is **yes, but only selectively**.

Tokamak plasma dynamics do **not** provide a new primary energy-storage mechanism for this project. Their strongest relevance is instead in:

- field symmetry and tolerance management;
- non-contact torque control;
- rotation-profile sensing and feedback;
- suppression/damping of destabilizing modes through controlled electromagnetic perturbations;
- maintaining a magnetically quiet region around sensitive suspension hardware.

The useful transfer is therefore **control and field-engineering methodology**, not plasma confinement itself.

---

## 1. Important distinction: plasma torus vs. solid rotor

A tokamak confines a conducting plasma using nested toroidal/poloidal magnetic fields. Its equilibrium and instability physics are governed by magnetohydrodynamics (MHD), plasma pressure, current profiles, magnetic shear, Alfvén continua, tearing modes, and wall interactions.

A mechanical flywheel/hoop rotor is instead governed by:

- elastic stress;
- inertia;
- bearing stiffness and damping;
- gyroscopic modes;
- rotor imbalance;
- structural fatigue;
- vacuum drag;
- electromagnetic drive forces.

Therefore, equations or stability claims from tokamak MHD **must not be copied directly** into the rotor model.

Transferable value comes from analogous engineering patterns.

---

## 2. Transferable tokamak principle A — Axisymmetry is a stability asset

Tokamak rotation and confinement are highly sensitive to non-axisymmetric field errors.

IAEA/PPPL work on toroidal plasma rotation shows that non-axisymmetric field errors can exert toroidal torque and alter rotation profiles. ITER also treats millimetre-scale coil-position errors as important enough to require detailed field-map reconstruction from as-built geometry.

### Implication for kinetic storage

The rotor/magnetic-bearing system should treat **electromagnetic axisymmetry as a first-class design variable**.

For the mechanical system this means:

- minimize motor/stator field harmonics near magnetic bearings;
- separate torque-production fields from the magnetic-bearing quiet zone;
- model assembly runout and stator eccentricity as force-ripple sources;
- create an as-built magnetic-field map for prototypes rather than relying only on nominal CAD geometry.

### Actionable research task

Add a future model:

`simulations/electromagnetics/field_error_forcing.py`

Inputs:
- rotor eccentricity;
- stator harmonic amplitudes;
- bearing stiffness;
- spin speed.

Outputs:
- synchronous radial force;
- sub/super-synchronous forcing terms;
- predicted displacement response near critical speeds.

This is directly relevant to C-005 and C-006.

---

## 3. Transferable tokamak principle B — Rotation profile control can stabilize or destabilize

Tokamak research treats toroidal rotation and **rotation shear** as variables that can modify stability and confinement.

A key warning from the literature is that high rotation is not automatically stabilizing: angular-velocity shear can also drive or worsen some modes.

### Implication for differential hoops

This is especially relevant to the project's differential-speed architecture.

Do **not** assume that different hoop speeds are always beneficial.

Differential speeds introduce:

- beat-frequency forcing;
- changing magnetic harmonics in neighboring zones;
- possible gas-shear / electromagnetic torque exchange;
- time-varying bearing loads.

### Actionable design rule

For any multi-zone rotor concept, characterize not only absolute RPM but:

- ΔRPM between adjacent zones;
- d(ΔRPM)/dt during acceleration;
- beat frequencies between motor harmonics;
- proximity of those frequencies to structural/bearing modes.

A future control system should avoid forbidden differential-speed bands in the same way rotating-plasma control avoids destabilizing operating regions.

---

## 4. Transferable tokamak principle C — Weak non-axisymmetric fields can provide controlled torque

Tokamak experiments use externally applied non-axisymmetric magnetic fields and neutral-beam torque to control toroidal rotation.

The analogous mechanical opportunity is:

> Use deliberately controlled, weak non-axisymmetric electromagnetic fields as a **contactless trim/damping actuator**.

This is not primary propulsion/storage.

It could be used for:

- active whirl damping;
- centering trim;
- controlled de-spin;
- compensation for rotor imbalance;
- suppression of a narrow resonant mode.

### Candidate concept

A low-authority electromagnetic damper consisting of segmented stator coils around the stationary housing.

Normal mode:
- near-zero average torque;
- phase-controlled small radial/tangential forces.

Fault mode:
- stronger damping command if vibration grows.

### Key caution

This only helps if actuator mass, coil heating, and rotor eddy-current losses stay small.

It should be explored only after the low-energy mechanical prototype establishes measurable vibration modes.

---

## 5. Transferable tokamak principle D — Field-error mapping from real geometry

ITER explicitly reconstructs magnetic fields from the **as-built, deformed positions** of its toroidal field coils because mechanical tolerances alter the actual magnetic field.

This is a powerful engineering lesson for the project.

### Prototype implication

For any magnetic-bearing/contactless-drive prototype:

1. measure actual rotor/stator concentricity;
2. record bearing/stator axial positions;
3. map field strength around the circumference;
4. feed those measurements back into the digital twin.

The digital twin should eventually contain an `as_built.json` input rather than assuming perfect geometry.

---

## 6. Transferable tokamak principle E — Rotating magnetic field / localized magnetic pressure

IAEA research has explored toroidal plasma equilibrium using a rotating magnetic field localized between plasma and shell.

The closest useful mechanical analogy is a **distributed magnetic braking or centering field near the rotor perimeter**.

Potential application:

- non-contact pre-contact braking;
- reduce energy before a rotor reaches a sacrificial catcher;
- magnetic centering near an excursion limit.

### Status

Interesting but **highly speculative** for this project.

Why:
- magnetic pressure has limited specific energy;
- conductive rotors can incur eddy losses;
- composite CNT/carbon structures may couple weakly unless conductive layers are intentionally added;
- the field hardware adds mass.

This concept should remain a research branch only until quantified.

---

## 7. What should NOT be transferred from tokamak physics

Do not import the following as direct design assumptions:

- plasma MHD equilibrium equations;
- plasma pressure balance as a substitute for mechanical containment;
- magnetic confinement as a replacement for structural rotor integrity;
- Alfvén-wave stabilization concepts as if a solid rotor were a plasma;
- plasma self-organization as evidence that many unbonded hoops will remain dynamically isolated.

Those mechanisms operate in a fundamentally different medium.

---

## 8. Most promising tokamak-derived opportunity

The strongest actionable idea is:

> **Use tokamak-style field-error awareness and active electromagnetic mode control to make the magnetic bearing / motor environment more axisymmetric and dynamically quiet.**

This could improve:

- HTS bearing AC-loss control;
- whirl damping;
- rotor centering;
- tolerance robustness;
- fault response.

It does **not** solve:

- CNT material feasibility;
- containment mass;
- 500 Wh/kg target;
- high-speed rotor burst safety.

---

## 9. Recommended experiments / models

### T-01 — Harmonic field-error forcing model
Low-risk software task.

Model how small stator asymmetry/eccentricity creates radial/tangential periodic forces.

### T-02 — Low-energy active magnetic damping rig
After P0/P1 low-energy rotor dynamics are working, add one small trim coil pair and measure whether vibration amplitude can be reduced.

### T-03 — As-built field map
For any future magnetic-bearing rig, map static field around 360 degrees and compare nominal vs. measured field harmonics.

### T-04 — Differential-speed forbidden-band map
Build a Campbell-like chart whose axes include:
- rotor A RPM;
- rotor B RPM;
- beat frequency;
- structural modes.

This is likely more useful to the present architecture than copying plasma-rotation equations.

---

## 10. Current recommendation

**Do not pivot the architecture to a tokamak-like storage mechanism.**

Instead, selectively import four tokamak engineering practices:

1. strict electromagnetic axisymmetry;
2. explicit field-error/tolerance modeling;
3. low-authority non-contact mode damping;
4. measured rotation-profile feedback.

These may become enabling control technologies if later prototypes use magnetic suspension and contactless torque transfer.

---

## Sources reviewed

- ITER: "Translating physics limits to millimetres" — precision/tolerance and as-built magnetic field mapping.
  https://www.iter.org/node/20687/translating-physics-limits-millimetres

- IAEA: "Toroidal Rotation in Tokamak Plasmas" — torque and rotation effects from resonant and non-resonant field errors.
  https://www-pub.iaea.org/mtcd/meetings/fec2008/th_p8-36.pdf

- Princeton Plasma Physics Laboratory / Nuclear Fusion: model-based control of plasma rotation in NSTX using neoclassical toroidal viscosity and neutral beam injection.
  https://nstx.pppl.gov/DragNDrop/Publications_Presentations/Publications/2016%20Papers/2016%20Locked/Goumiri_NF.pdf

- PPPL: rotation-modified MHD continuum and Alfvén-mode stability.
  https://www.pppl.gov/events/2026/linear-perturbative-ideal-mhd-formulation-and-mhd-continuum-including-toroidal-rotation

- IAEA Fusion Energy Conference: plasma confinement by pressure of a rotating magnetic field in a toroidal device.
  https://conferences.iaea.org/event/46/contributions/8160/
