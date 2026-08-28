# P0 Digital Twin Result

A reduced-order digital twin has been added for the exact three-ring benchtop prototype geometry.

## Reference rotor properties

At 1200 kg/m^3 polycarbonate density:

- Rotor A (300/270 mm, 6 mm): ~96.7 g
- Rotor B (240/210 mm, 6 mm): ~76.3 g
- Rotor C (180/150 mm, 6 mm): ~56.0 g

Total kinetic energy at the 300 RPM hard command limit is approximately **1.63 J**.

## Controller model

Each zone uses:
- first-order brushed-DC motor torque/back-EMF model
- individual PI speed loop
- independent inertia
- viscous drag
- 300 RPM command clamp
- latched overspeed/vibration fault model

## Virtual commissioning result

The model reaches the representative 180/120/60 RPM differential operating point within the project's ±5% steady-state tracking criterion.

This does not prove physical stability; it confirms that the proposed low-speed motor sizing/control concept is internally consistent enough to proceed to the P0-A/P0-B physical build milestones.

## Next physical result required

The project now needs a real P0-A mechanical dummy, followed by one powered zone. No higher-energy rotor experiment is justified until those two milestones pass.
