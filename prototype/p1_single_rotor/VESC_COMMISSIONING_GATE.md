# P1 VESC Commissioning Gate

## Purpose

Prevent a controller configuration or drivetrain conversion error from silently authorizing operation outside the released low-energy P1 envelope.

Before a powered run, the intended controller/supervisor settings must be represented by `vesc_config_gate.py` and pass `validate_commissioning_config()`.

## Released invariants

- rotor command limit: <=1500 RPM
- independent rotor overspeed trip: <=1650 RPM
- battery discharge current limit: <=5 A
- regenerative battery-current limit: <=1 A
- regenerative test bus window: 24-28 V
- motor: 14 poles / 7 pole pairs
- timing drive: 15T motor pulley, 48T rotor-shaft pulley

## Speed conversion

The VESC observes motor electrical speed rather than rotor RPM.

With the released 15:48 timing ratio:

- motor RPM = rotor RPM x 48/15 = rotor RPM x 3.2
- ERPM = motor RPM x 7 pole pairs

Therefore:

- 1500 rotor RPM = 4800 motor RPM = **33,600 ERPM**
- 1650 rotor RPM = 5280 motor RPM = **36,960 ERPM**

The VESC electrical-speed ceiling is not the safety trip. The independent rotor-speed supervisor remains authoritative for overspeed detection.

## Pre-power record

Record a screenshot/export or written transcription of the actual controller settings used for the run. The record must include at least:

- motor current limit(s)
- battery discharge-current limit
- battery regenerative-current limit
- ERPM / speed-control limit used by the controller
- motor pole count or detected motor parameters
- firmware version
- controller hardware revision
- measured DC-bus voltage before enable

A run is not an acceptance run if the settings record is missing.

## Dry validation

Run:

```bash
python prototype/p1_single_rotor/vesc_config_gate.py
```

Expected released result:

```text
command limit: 1500 rotor RPM = 33600 ERPM
overspeed trip: 1650 rotor RPM = 36960 ERPM
P1 commissioning configuration: PASS
```

Then dry-test the independent supervisor using injected/simulated speed values as already specified in the supervisor commissioning procedure. Do not perform a physical overspeed test.

## Change control

Any configuration that requires increasing rotor speed above 1500 RPM, the overspeed threshold above 1650 RPM, battery discharge above 5 A, regen above 1 A, or expanding the released bus window is outside P1. Such a change requires a new reviewed engineering decision and is not authorized by this document.
