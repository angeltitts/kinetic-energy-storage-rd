# P1 Bill of Materials

The controlled exact safety/instrumentation procurement references and substitution rules are in `EXACT_PROCUREMENT_RELEASE_V1.md`. Use that document for S1, K1, F1, passive dump, RPM pickup and instrumentation ordering.

## Core drive/electronics

1. **Sensored BLDC motor** — Flipsky 5055 200KV 1500W class or released equivalent; measure delivered motor face before drilling.
2. **VESC-compatible controller** — Mini FSESC 4.20 50A class is sufficient for this low-energy rig when current-limited.
3. **DC source/sink** — retained primary is Bioenno BLF-2410AS, 24 V / 10 Ah LiFePO4 with built-in PCM. A generic "6S battery" is not an equivalence rule.
4. **Emergency stop S1** — primary AutomationDirect GCX3131, latching twist-reset, 1 NC.
5. **Isolation relay K1** — primary Picker PC792A-1C-C2-24C-N-X, 24 VDC coil, >=20 A class DC contact.
6. **Main fuse F1** — 10 A ATO/ATC in a >=32 VDC holder; primary Littelfuse FHAS100 + 0ATO010.VPGLO.
7. **Passive dump** — Ohmite HS100 22R J, 22 ohm / 100 W chassis mount or validated equivalent.
8. **Independent RPM sensor** — EE-SX1042-class optical pickup with the released 12-feature target; independent of VESC telemetry.
9. **Accelerometer** — MPU6050-class frame-mounted 3-axis sensor.
10. **DC power cross-check** — INA226-class bidirectional monitor rated >=36 V and >=5 A; verify actual shunt calibration.
11. **Temperature** — four contact probes for bearings/motor/VESC plus K-type thermocouple on dump-resistor chassis.

## Mechanical

1. 6061-T6 aluminum rotor disk, 200 mm x 6 mm.
2. 12 mm precision steel shaft, nominal 260 mm.
3. 2 x KP001-class 12 mm pillow-block bearings.
4. Custom split-clamp rotor hub for 12 mm shaft.
5. HTD 5M belt drive: 15T motor pulley / 48T rotor pulley, 15 mm width, 400 mm belt.
6. 400 x 300 x 12 mm minimum rigid base plate.
7. 6 mm minimum clear polycarbonate 360-degree rotor guard; acrylic is not a substitute.
8. Fasteners, removable threadlocker, shaft collars, cable clamps and covered terminals.

## Frozen P1 procurement constraints

- command speed <=1500 RPM
- independent overspeed trip >=1650 RPM
- battery discharge <=5 A during commissioning
- regenerative battery current <=1 A
- F1 exactly 10 A maximum
- passive dump remains 22 ohm / >=100 W across the controller-side bus
- no powered operation without the complete guard

Prices and stock change. `EXACT_PROCUREMENT_RELEASE_V1.md` records dated references, but ratings and incoming inspection—not lowest price—control substitution acceptance.
