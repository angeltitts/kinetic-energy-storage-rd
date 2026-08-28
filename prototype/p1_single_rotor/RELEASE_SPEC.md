# P1 Manufacturing Release v1.0

## Frozen mechanical envelope

Rotor:
- 6061-T6 aluminum
- 200 mm OD
- 6 mm thickness
- 12 mm center bore through clamping hub assembly
- target static balance: no persistent heavy-side settling after hand rotation
- target radial runout at OD: <=0.25 mm
- target axial wobble at OD: <=0.25 mm

Shaft:
- 12 mm precision steel shaft
- minimum straight unsupported rotor span kept as short as practical
- two 12 mm pillow-block bearings

Base:
- minimum 400 x 300 x 12 mm aluminum or rigid steel plate

Guard:
- clear polycarbonate, >=6 mm wall near rotor plane
- 360-degree rotor enclosure
- minimum 50 mm radial clearance from rotor OD
- no powered operation without guard

## Drive

Preferred initial hardware:
- sensored BLDC outrunner, ~200 KV
- VESC-compatible bidirectional controller
- motor mechanically coupled to rotor shaft
- independent optical or magnetic RPM pickup in addition to motor commutation telemetry

## Electrical limits

- nominal DC bus: 18-26 V
- current limit during first commissioning: 5 A
- increase only after thermal and mechanical checks, never beyond controller/motor limits
- command speed limit: 1500 RPM
- overspeed trip: 1650 RPM

## Acceptance gates

P1-A mechanical:
- free hand rotation
- runout/wobble within tolerance
- no guard interference

P1-B motoring:
- 250 / 500 / 750 / 1000 / 1250 / 1500 RPM
- hold each point for 30 s
- no abnormal vibration growth

P1-C coast-down:
- accelerate to 1500 RPM
- remove drive torque
- log RPM until 300 RPM
- derive equivalent loss power vs speed

P1-D regeneration:
- accelerate to 1500 RPM
- command controlled regenerative deceleration to 300 RPM
- log DC-bus voltage/current
- calculate recovered electrical energy

P1-E repeatability:
- 20 charge/discharge cycles
- no loose hardware, temperature excursion, or growing vibration
