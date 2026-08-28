# P0 Working Prototype Build Sequence

## Milestone P0-A — Mechanical dummy

Build the three annular polycarbonate rotors and stacked support planes without motors.

Acceptance:
- all three rotate freely by hand;
- no rotor-to-rotor contact;
- at least 15 mm axial separation between rotating planes;
- transparent guard can close without interference.

## Milestone P0-B — Single powered zone

Install one gearmotor, friction wheel, Hall sensor, driver, fuse, and physical E-stop.

Acceptance:
- stable 50/100/150/200 RPM operation;
- measured RPM agrees with handheld tachometer if available;
- physical E-stop removes motor power immediately.

## Milestone P0-C — Three-zone powered rig

Add channels B and C.

Acceptance:
- independent command and sensing;
- differential run at 180/120/60 RPM for 60 s;
- differential run at 100/200/150 RPM for 60 s;
- no mechanical contact.

## Milestone P0-D — 10-minute demonstration

Run 180/120/60 RPM for 10 minutes with CSV logging.

Acceptance:
- each rotor remains within ±5% of target after settling;
- no latched fault;
- no visible fastener migration or motor-bracket movement;
- controlled STOP completes without contact.

## Digital twin

Before hardware commissioning, run:

    python prototype/p0/run_virtual_commissioning.py

The current reduced-order model should pass the same ±5% steady-state tracking target.

The digital twin is not a substitute for physical testing; it is a controller/mechanics sanity check.
