# P0 Assembly and Commissioning Checklist

## Before power

- [ ] Guard installed around the full rotor stack
- [ ] Emergency-stop switch interrupts motor supply directly
- [ ] Fuse installed in motor supply
- [ ] All rotor edges deburred
- [ ] Rotor planes separated by at least 15 mm
- [ ] No rotor can contact another rotor by hand deflection
- [ ] Motor brackets secure
- [ ] Hall sensor wiring secured away from moving parts
- [ ] Rotor magnets mechanically retained
- [ ] Base clamped or bolted to bench

## First power-up

- [ ] Motor supply current-limited if available
- [ ] One motor connected at a time initially
- [ ] Verify correct rotation direction
- [ ] Verify Hall RPM at hand rotation
- [ ] Verify E-stop at zero speed
- [ ] Verify software fault latch with simulated overspeed value

## First rotating test

Run each rotor independently:
- [ ] 50 RPM for 30 s
- [ ] 100 RPM for 30 s
- [ ] 150 RPM for 30 s
- [ ] 200 RPM for 30 s

Stop if there is:
- visible wobble
- rubbing/contact
- loosening hardware
- sensor dropout
- abnormal vibration increase

## Differential test

- [ ] A=180, B=120, C=60 RPM for 60 s
- [ ] A=100, B=200, C=150 RPM for 60 s
- [ ] Log measured RPM
- [ ] Log vibration
- [ ] Verify no speed entrainment between zones

## Endurance demonstration

After all previous steps pass:

- [ ] A=180, B=120, C=60 RPM
- [ ] Run continuously for 10 minutes
- [ ] Record CSV log
- [ ] Confirm each rotor stays within ±5% target
- [ ] Controlled stop
- [ ] Inspect hardware after stop

A completed 10-minute differential run with clean logs constitutes the first working P0 architecture prototype.
