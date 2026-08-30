# Hybrid Power Buffer Architecture v1

## Objective

Evolve the commercial track from a standalone flywheel into a **battery-protection power buffer**.

The flywheel handles short, high-C-rate transients and regenerative pulses.
The battery handles longer-duration energy demand and state-of-charge support.

## System topology

Grid / DC source
    |
Bidirectional DC bus
    |---------------- Battery pack + BMS
    |---------------- Flywheel module + bidirectional inverter
    |---------------- Load / regenerative source

## Control objective

At every control step, split requested load power between flywheel and battery such that:

1. flywheel absorbs fast-changing power;
2. battery power changes more slowly;
3. flywheel state-of-charge stays near a configurable reserve band;
4. regenerative power is preferentially absorbed by the flywheel when headroom exists;
5. battery and flywheel current/power limits are never exceeded;
6. faults force a safe fallback to battery/grid-only operation.

## Flywheel state of charge

For a rotor:

    E = 0.5 I omega^2

Define:

    SOC_fw = (E - E_min) / (E_max - E_min)

For the P1 hardware this is only a control-development proxy. Commercial values will be set later.

## Dispatch strategy v1

Use a low-pass filtered version of load power as the battery target.

    P_batt_target = LPF(P_load)

The flywheel handles the residual:

    P_fw_target = P_load - P_batt_target

Then bias the flywheel command toward its reserve SOC target:

    P_fw_cmd = P_fw_target + K_soc * (SOC_fw - SOC_target)

Sign convention:
- positive power = delivering power to the load
- negative power = absorbing regenerative power

Finally clamp both power commands to hardware limits.

This architecture deliberately avoids claiming novel patentability. It is an engineering baseline for measured optimization.

## Why this is useful

A battery-only system sees every transient.

A hybrid system can reduce:
- battery current peaks;
- battery dP/dt;
- high-frequency microcycles;
- thermal excursions;
- peak grid demand.

The flywheel is not required to beat lithium-ion in Wh/kg. It must reduce lifetime stress and power-system oversizing enough to justify its cost.

## P2/P3 data that will improve this controller

P1:
- measured electrical round-trip efficiency;
- coast-down loss vs RPM;
- regen stability;
- converter efficiency;
- vibration limits.

P2:
- windage loss reduction under reduced pressure.

P3:
- bearing-loss reduction.

These measurements will replace the placeholder flywheel-efficiency model.

## Commercial control metrics

Track:
- battery peak power reduction;
- battery RMS power reduction;
- battery power slew reduction;
- flywheel energy throughput;
- flywheel SOC reserve violations;
- curtailed regenerative energy;
- system round-trip energy loss.

## Patent opportunity screening

Potentially differentiated areas to investigate later:
- predictive dispatch using measured battery impedance/temperature;
- flywheel health-aware power derating;
- automatic resonance-zone avoidance;
- dispatch based on battery degradation cost rather than only power filtering;
- learned prediction of repetitive industrial load cycles.

Do not file broad claims around generic battery-flywheel hybridization without a prior-art search.
