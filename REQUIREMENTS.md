# Requirements

## Phase 0 feasibility requirements

### R-001 — System specific energy
Target: >= 500 Wh/kg complete system.

This is now treated as a **competitive threshold**, not merely a theoretical milestone. Advanced silicon-anode lithium-ion cells have demonstrated >500 Wh/kg at the cell level. DSHC must therefore justify itself on complete-system energy density plus at least one major system advantage such as cycle life, power density, recharge rate, self-discharge, safety/service life, or cost.

### R-001A — Competitive benchmark
The project must maintain a benchmark table against state-of-the-art electrochemical storage. At minimum compare:
- Wh/kg
- Wh/L
- cycle life
- round-trip efficiency
- standby loss
- peak/continuous power density
- charge rate
- thermal operating envelope
- safety/containment burden
- manufacturing maturity
- estimated cost/kWh when defensible data exist

Initial benchmark source: `research/benchmarks/amprius_500whkg.md`.

### R-002 — Material baseline
Evaluate a hypothetical structural CNT material at:
- usable static tensile strength: 20 GPa
- density: 1,500 kg/m^3

The model must separately expose:
- fatigue derating
- engineering safety factor

### R-003 — Complete mass accounting
At minimum include:
- rotor mass
- containment mass
- vacuum housing mass
- motor/generator stator mass
- bearing mass
- cryogenic mass
- power electronics mass
- controls/sensors allowance

### R-004 — Tip speed
Always report peripheral velocity and RPM.
Radius must never be treated as changing required peripheral speed for a given hoop stress.

### R-005 — Safety accounting
Containment cannot be omitted from system Wh/kg.

### R-006 — Failure honesty
A concept that fails the 500 Wh/kg gate under defensible assumptions must be reported as failing.

### R-007 — No false parity
Rotor-only energy density must never be compared directly to electrochemical cell or pack energy density. Comparisons must be made at clearly labeled levels: active material, rotor/cell, module, and complete system/pack.

## Future requirements — placeholders
- cycle life
- standby loss
- maximum allowable rotor temperature
- maximum module stored energy
- manufacturability tolerances
- cost per kWh
- service interval
- failure containment certification path
