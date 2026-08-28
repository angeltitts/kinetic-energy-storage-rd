# Phase 2 Result — Non-Rotor Mass Budget

## Question

At the 500 Wh/kg complete-system target, how much mass is actually available for containment, vacuum structure, stator, bearings, cryogenics, electronics, and controls?

## Core result

For the current reference material assumption (20 GPa raw strength, rho=1.5 g/cc, SF=1.5), the allowed total non-rotor mass is extremely sensitive to fatigue retention.

| Fatigue retention | Effective stress | Rotor Wh/kg | Maximum total non-rotor mass / rotor mass |
|---:|---:|---:|---:|
| 55% | 7.33 GPa | 679 | 0.358 |
| 60% | 8.00 GPa | 741 | 0.481 |
| 65% | 8.67 GPa | 802 | 0.605 |
| 70% | 9.33 GPa | 864 | 0.728 |
| 75% | 10.00 GPa | 926 | 0.852 |

## Containment budget at the 65% fatigue-retention threshold

At 65% fatigue retention, the total non-rotor allowance is only ~0.605 kg per kg of rotor.

If the rest of the machine consumes:

| Vacuum + stator + bearing/cryo + electronics + controls | Maximum containment mass / rotor mass |
|---:|---:|
| 0.25 | 0.355 |
| 0.35 | 0.255 |
| 0.45 | 0.155 |
| 0.55 | 0.055 |

## Interpretation

This tightens the Phase 1 conclusion considerably.

At the representative 65% fatigue-retention case, a conventional containment philosophy where the containment shell approaches the rotor mass is incompatible with a 500 Wh/kg complete-system target.

If non-containment subsystems require ~0.45 kg per kg of rotor, containment must be approximately **0.155 kg per kg of rotor or less**.

That is an aggressive requirement.

At only 60% fatigue retention, the total non-rotor allowance falls to ~0.481. If other subsystems consume 0.45, essentially no credible containment mass remains.

At 55% fatigue retention, any architecture with ~0.45 non-containment overhead is mathematically unable to reach 500 Wh/kg before containment is added.

## New design rule

> The project cannot treat containment and fatigue as separate optimization problems. They trade directly against the same system-mass budget.

## Working mass-allocation target

For continued concept development, use this **aggressive but explicit provisional target** at the 500 Wh/kg gate:

- rotor: 1.00 mass unit
- containment + sacrificial catcher: <= 0.15
- vacuum housing: <= 0.08
- motor/generator stator: <= 0.12
- bearing + cryogenic hardware: <= 0.08
- power electronics: <= 0.07
- controls/sensors/wiring: <= 0.03

Total non-rotor target: <= 0.53 mass units.

This leaves ~0.075 mass units of margin below the 0.605 theoretical limit for the 65% fatigue case.

These allocations are **targets, not validated estimates**. The next phase must determine whether any credible containment and drivetrain architecture can actually satisfy them.

## Consequence

The project's practical 500 Wh/kg feasibility now depends on two especially sharp quantities:

1. long-life usable fatigue retention must remain near or above ~65% of the assumed 20 GPa raw strength at SF=1.5;
2. containment must become a graceful-failure/capture system with mass far below conventional full-energy burst armor.

## Next kill question

> Is there a physically credible failure-management architecture whose required containment/catcher mass is <= ~0.15 rotor mass while keeping the expected failure trajectory safe?

If the answer is no, the current 20 GPa / 500 Wh/kg architecture should be rejected or the material-performance requirement must be increased.