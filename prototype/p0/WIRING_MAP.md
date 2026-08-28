# P0 Wiring Map

This is the low-energy three-zone benchtop prototype wiring map.

## Controller pins

| Function | RP2040/Pico pin |
|---|---:|
| Hall sensor A | GP2 |
| Hall sensor B | GP3 |
| Hall sensor C | GP4 |
| PWM motor A | GP6 |
| PWM motor B | GP7 |
| PWM motor C | GP8 |
| Direction A | GP9 |
| Direction B | GP10 |
| Direction C | GP11 |

## Power path

12 V supply -> fuse -> physical emergency-stop -> motor-driver supply.

The emergency-stop must remove motor power independently of firmware.

The Pico/controller remains on USB/logic power so telemetry can continue after a motor-power E-stop.

## Sensor wiring

Each Hall sensor:
- VCC to approved logic voltage
- GND to controller ground
- signal to its assigned GPIO
- one mechanically retained magnet/index marker per rotor

## Motor-driver requirement

Use three independently controllable brushed-DC H-bridge channels sized above the selected gearmotor stall current.

Do not connect a motor directly to a Pico GPIO.

## Commissioning order

1. power controller only;
2. verify Hall pulses by hand rotation;
3. verify all PWM outputs are zero at boot;
4. power one motor channel through the fused E-stop path;
5. verify direction and STOP behavior;
6. repeat for channels B/C;
7. install guard before any three-rotor run.
