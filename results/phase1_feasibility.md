# Phase 1 Feasibility Result — 500 Wh/kg Gate

## Result

The original conservative Phase 0 baseline fails the 500 Wh/kg complete-system target:

- raw material strength: 20 GPa
- density: 1,500 kg/m³
- fatigue retention: 50%
- safety factor: 1.5
- effective design stress: 6.67 GPa
- rotor specific energy: ~617 Wh/kg
- complete-system estimate: ~258 Wh/kg

Phase 1 reverses the problem: rather than guessing subsystem masses and asking what energy density results, it asks what effective hoop stress is required for a specified total non-rotor mass fraction.

For a thin hoop:

    e_rotor = sigma_eff / (2 rho)

    e_system = e_rotor / (1 + M_nonrotor / M_rotor)

For a 500 Wh/kg complete-system target at rho = 1,500 kg/m³:

| Total non-rotor mass / rotor mass | Required effective stress | Required fatigue retention with 20 GPa raw strength and SF=1.5 | Tip speed |
|---:|---:|---:|---:|
| 0.40 | 7.56 GPa | 56.7% | 2.24 km/s |
| 0.50 | 8.10 GPa | 60.8% | 2.32 km/s |
| 0.60 | 8.64 GPa | 64.8% | 2.40 km/s |
| 0.70 | 9.18 GPa | 68.9% | 2.47 km/s |
| 0.80 | 9.72 GPa | 72.9% | 2.55 km/s |
| 1.00 | 10.80 GPa | 81.0% | 2.68 km/s |
| 1.45 | 13.23 GPa | 99.2% | 2.97 km/s |

## Interpretation

A 500 Wh/kg DSHC is not ruled out by the thin-hoop equation under a hypothetical 20 GPa macroscale material, but it requires a narrow system-level design window.

A representative threshold case is:

- total non-rotor mass <= ~0.60 kg per kg of rotor
- effective hoop stress >= ~8.64 GPa
- with 20 GPa raw strength and SF=1.5, fatigue retention >= ~65%
- tip speed ~2.4 km/s
- RPM at 0.5 m radius ~45,800

This is the first useful design result from the program:

> The 500 Wh/kg gate is no longer primarily an energy equation problem. It is a coupled fatigue + parasitic-mass + hypervelocity rotordynamics problem.

## Competitive implication

The Amprius benchmark means 500 Wh/kg is only worth pursuing if DSHC can reach that level at the complete-system level and then beat advanced electrochemistry in at least one major dimension such as cycle life, power, recharge rate, self-discharge, service life, or cost.

## Current conclusion

**Conditional feasibility, low confidence.**

The concept survives the analytical gate, but only if all three conditions are demonstrated:

1. macroscale structural material retains roughly 65% or more of a 20 GPa raw tensile strength under long-life cyclic operation at an engineering safety factor near 1.5;
2. complete non-rotor mass can be held near or below ~60% of rotor mass;
3. stable, controllable operation around 2.4 km/s peripheral speed is possible.

Failure of any one of these conditions pushes the 500 Wh/kg target out of reach at the assumed material strength.

## Next critical question

Do not optimize the HTS bearing or actuator first.

The next kill question is:

> Can a believable complete containment + vacuum + stator + bearing + cryogenic + electronics architecture stay below ~0.60 kg of non-rotor mass per kg of rotor while providing a safe failure path?

Until that is answered, detailed motor or bearing optimization is premature.