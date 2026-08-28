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
- four mechanically retained magnet/index markers per rotor
- magnets equally spaced at 90 degrees and at the same radius

The firmware assumes exactly four pulses per mechanical revolution. Verify exactly four clean transitions per hand-turned revolution before motor power is enabled.

Why four: the acceptance plan includes 50 RPM. One pulse/revolution gives a 1.20 s interval at 50 RPM, which exceeded the prior 1.0 s stale-speed timeout. Four pulses/revolution reduce the interval to 0.30 s and support low-speed closed-loop validation without increasing rotor speed.

## Motor-driver requirement

Use three independently controllable brushed-DC H-bridge channels sized above the selected gearmotor stall current.

Do not connect a motor directly to a Pico GPIO.

## Commissioning order

1. power controller only;
2. verify exactly four Hall pulses per hand-turned revolution on A, B, and C;
3. verify all PWM outputs are zero at boot;
4. power one motor channel through the fused E-stop path;
5. verify direction and STOP behavior;
6. verify stable telemetry at the 50 RPM acceptance point;
7. repeat for channels B/C;
8. install guard before any three-rotor run.
