# P1 Single-Rotor Energy-Recovery Prototype

Status: **READY FOR LOW-ENERGY FABRICATION**

This is the first prototype on the patent-conscious commercial track.

It intentionally does **not** use:
- nested rotors
- HTS bearings
- cryogenics
- high-speed composite rotors
- vacuum
- destructive testing

## What it proves

P1 proves the product's most important electrical/mechanical loop:

> electrical energy -> motor/generator -> rotor kinetic energy -> controlled regenerative discharge -> electrical energy

It also measures:
- spin-up time
- coast-down loss
- regenerative energy recovery
- closed-loop speed control
- bearing/friction losses
- vibration trend
- emergency shutdown behavior

## Reference rotor

6061-T6 aluminum disk:
- diameter: 200 mm
- thickness: 6 mm
- mass: ~0.509 kg
- inertia: ~0.002545 kg·m²
- command limit: 1500 RPM
- overspeed trip: 1650 RPM
- stored energy at 1500 RPM: ~31.4 J
- stored energy at 1650 RPM: ~38.0 J

This is deliberately a low-energy prototype.

## Architecture

Horizontal 12 mm steel shaft supported by two pillow-block bearings.
The aluminum rotor disk is clamped to the shaft through a machined hub.
A sensored BLDC motor is coupled to the shaft through a flexible coupling or 1:1 belt.
A VESC-compatible controller handles motoring and regenerative braking.
A 6S battery/safe DC sink-source bus absorbs regenerated energy.

A full polycarbonate guard surrounds the rotor and shaft.
