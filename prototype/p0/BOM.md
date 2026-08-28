# P0 Bill of Materials

Quantities are for one three-zone rig.

## Mechanical

| Qty | Item | Functional requirement |
|---:|---|---|
| 1 | 300/270 mm polycarbonate annulus | 6 mm thick |
| 1 | 240/210 mm polycarbonate annulus | 6 mm thick |
| 1 | 180/150 mm polycarbonate annulus | 6 mm thick |
| 3 | low-speed turntable/lazy-Susan bearings | one per rotor plane |
| 3 | stationary spacer plates | plywood, aluminum, or rigid polymer |
| 3 | tangential motor brackets | adjustable spring pressure |
| 3 | rubber/polyurethane drive wheels | approx. 20–35 mm diameter |
| 1 | rigid base plate | approx. 450 x 450 mm |
| 1 | transparent polycarbonate guard | surrounds all rotating parts |
| assorted | screws, spacers, washers, threadlocker | mechanical assembly |

## Drive

| Qty | Item | Functional requirement |
|---:|---|---|
| 3 | 12 V brushed DC gearmotors | 300–500 RPM output range |
| 3 | H-bridge motor channels | rated above motor stall current |
| 1 | 12 V DC supply | sized for all three motors |
| 1 | emergency-stop switch | directly interrupts motor power |
| 1 | inline fuse | sized to motor supply |

## Control and sensing

| Qty | Item | Functional requirement |
|---:|---|---|
| 1 | Raspberry Pi Pico / RP2040 board | main controller |
| 3 | Hall-effect digital sensors | one per rotor |
| 3 | small magnets | rotor index markers |
| 1 | 3-axis accelerometer module | frame vibration |
| 1 | USB cable | power/program/logging |
| 1 | breadboard or perfboard | prototype wiring |
| assorted | connectors/wire | low-voltage wiring |

## Optional

- small OLED display for RPM/fault state
- thermistors on motors
- SD-card logger
- current sensors for each motor

## Fabrication note

The annular rotors can be:
- CNC-routed
- waterjet-cut
- laser-cut if the fabricator supports polycarbonate safely
- carefully machined from sheet stock

Edges should be deburred and balanced before use.
