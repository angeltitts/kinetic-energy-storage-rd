# Assumptions Register

Every assumption is provisional until replaced by measured or high-quality published evidence.

| ID | Assumption | Baseline | Status |
|---|---|---:|---|
| A-001 | CNT structural density | 1500 kg/m^3 | hypothetical baseline |
| A-002 | CNT usable tensile strength before fatigue/SF | 20 GPa | hypothetical baseline |
| A-003 | fatigue derating multiplier | 0.50 | uncertain |
| A-004 | engineering safety factor | 1.50 | provisional |
| A-005 | thin hoop model | sigma=rho*v^2 | analytical |
| A-006 | containment/rotor mass ratio | 0.50–2.00 sweep | unresolved |
| A-007 | non-containment parasitic mass | explicit sweep | unresolved |
| A-008 | no shaft required | architecture target | unvalidated |
| A-009 | HTS bearing feasible | concept-level only | low confidence |

## Effective stress
The Phase 0 model defines:

    sigma_effective = sigma_material * fatigue_derating / safety_factor

This is deliberately conservative and easy to change.
