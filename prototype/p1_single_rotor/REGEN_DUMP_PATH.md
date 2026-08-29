# P1 Passive Regenerative Dump Path

## Problem closed by this release

The selected LiFePO4 battery has an internal PCM/BMS. During regenerative braking, a battery that is full or whose protection circuit opens can stop accepting current while the motor/controller is still returning energy to the DC bus. The P1 rotor stores only about 38 J at the released overspeed threshold, but that energy still needs a deterministic low-energy sink.

The P1 electrical release therefore adds a passive resistive dump branch on the **controller side of the battery contactor**.

## Released dump element

Use:
- 22 ohm nominal resistance
- 100 W minimum chassis-mount power rating
- non-inductive or low-inductance resistor construction preferred
- bolt the resistor to the metal base plate with thermal compound/pad as appropriate for the purchased part
- protect terminals against accidental contact

The resistor is connected directly across the VESC DC bus node, downstream of the battery fuse/contactor.

This means the dump resistor remains electrically across the controller bus even if the battery contactor opens.

## Quantitative check

At the released 1.0 A maximum regenerative battery-current command:

- 24.0 V bus: resistor current = 1.091 A, dissipation = 26.18 W
- 25.6 V bus: resistor current = 1.164 A, dissipation = 29.79 W
- 28.0 V bus: resistor current = 1.273 A, dissipation = 35.64 W
- 29.2 V bus: resistor current = 1.327 A, dissipation = 38.76 W

Therefore, throughout the released 24-28 V regenerative-test window, the passive resistor alone draws more than the 1.0 A permitted regenerative current. Under the first-test current limit, regeneration can be absorbed on the DC bus without requiring net battery charging.

The 100 W resistor operates below 40% of nameplate power even at 29.2 V. Actual allowable continuous dissipation still depends on the purchased resistor's mounting and thermal derating instructions, so baseplate temperature must be observed during commissioning.

## Wiring topology

Battery positive -> 10 A fuse -> E-stop controlled contactor -> P1 DC BUS + -> VESC +

Battery negative ------------------------------------------> P1 DC BUS - -> VESC -

22 ohm / >=100 W dump resistor is connected between P1 DC BUS + and P1 DC BUS -.

The independent VESC-branch current measurement used for recovered-energy accounting must be between the common DC bus and the VESC branch. Do **not** infer regenerated energy from battery-terminal current because the dump branch intentionally diverts returned energy before it reaches the battery.

## Regen enable conditions

For initial P1 regenerative tests:
- DC bus must be 24.0-28.0 V before regen is enabled;
- VESC regenerative battery-current command remains <=1.0 A magnitude;
- dump resistor must be physically installed and thermally mounted;
- independent bus voltage measurement must be active;
- battery must not be at full state of charge;
- stop if bus voltage exits the released window, the resistor mount overheats, or the supervisor latches any fault.

## What this does and does not prove

This is a low-energy protective load and measurement aid for P1. It is not a production braking chopper, not a certified battery charge controller, and not authorization for higher regenerative current or higher stored energy.

A future product-level DC bus requires a purpose-designed bidirectional power stage / braking chopper and formal electrical safety review.

## Evidence basis

Bioenno's current BLF-2410AS product page specifies a 24 V / 10 Ah pack, 10 A continuous discharge, built-in PCM protection, and a recommended 29.2 V / 2 A charger. Bioenno's current FAQ recommends charging LiFePO4 packs at no more than 0.5C for cycle life. The released 1 A P1 regen limit is 0.1C for a 10 Ah pack and remains conservative, while the passive dump removes dependence on the battery accepting that current during the first prototype tests.

Flipsky's published Mini FSESC4.20 specifications list an 8-60 V operating range and 60,000 ERPM limit. The passive dump does not alter those controller limits or the P1 mechanical envelope.
