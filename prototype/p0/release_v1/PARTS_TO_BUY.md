# Parts to Buy — P0 Release v1.0

## Electronics
- 1x Raspberry Pi Pico H (pre-soldered headers preferred)
- 3x PWM+DIR brushed DC motor driver carriers, MAX14870-class, 12 V, >=3 A peak
- 3x 12 V 25 mm metal gearmotors, 300-500 RPM no-load, stall current <=2.5 A
- 3x 20-35 mm rubber/polyurethane friction wheels matching motor shaft
- 3x digital Hall sensor modules, 3.3 V compatible
- 12x 5-8 mm neodymium magnets with mechanical retention (4 equally spaced per rotor)
- 1x 3-axis accelerometer module, I2C, 3.3 V compatible
- 1x 12 V / 5 A regulated supply
- 1x 5 A inline fuse holder + spare fuses
- 1x 22 mm normally-closed latching mushroom E-stop
- 1x USB cable for Pico
- 1x terminal block / distribution board
- 2 m 18 AWG stranded wire
- 3 m 22-24 AWG hookup wire
- ferrules, crimp terminals, heat-shrink, cable ties

## Hall index installation
- install 4 magnets per rotor at equal 90-degree spacing
- keep the four magnets on a rotor at the same radius
- use equivalent magnet size/orientation and mechanical retention
- verify exactly four clean Hall transitions per hand-turned revolution before motor power is enabled

Four pulses/revolution are required because the release acceptance tests extend down to 50 RPM; at one pulse/revolution, a valid 50 RPM signal arrives only every 1.20 s and is too sparse for the firmware/control timeout.

## Mechanical
- 1x 450 x 450 x 10 mm aluminum or HDPE base plate
- 1x 6 mm clear polycarbonate sheet, minimum 320 x 700 mm usable area
- 3x low-play turntable/lazy-Susan bearing rings sized to support the rotor planes
- 3x stationary support plates
- 4x vertical guard/support posts, ~300-350 mm
- 1x clear polycarbonate guard, cylindrical or box type, >=3 mm wall
- 3x adjustable motor brackets
- assorted M3/M4/M5 fasteners, nyloc nuts, washers, spacers
- medium-strength removable threadlocker
- rubber feet for base

## Fabrication services
Ask a CNC router or waterjet shop for three annular polycarbonate parts:
- 300/270/6 mm
- 240/210/6 mm
- 180/150/6 mm

Requirements:
- deburr all edges
- no cracks/chips
- OD concentric to ID within 0.25 mm preferred
- flatness sufficient to keep axial wobble <=0.75 mm after mounting

Do not laser-cut polycarbonate unless the fabrication shop explicitly supports it and can produce clean, crack-free parts.
