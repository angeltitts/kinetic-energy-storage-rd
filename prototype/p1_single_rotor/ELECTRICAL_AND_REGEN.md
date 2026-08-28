# Electrical / Regenerative Energy Path

## Charge

DC bus -> VESC -> BLDC motor/generator -> shaft -> flywheel rotor

The controller accelerates the rotor under a current and RPM limit.

## Store

At target RPM the controller commands near-zero torque.
Measured coast-down rate quantifies bearing, windage, motor, and electrical drag.

## Discharge

Flywheel rotor -> BLDC motor/generator -> VESC regenerative braking -> DC bus

The DC bus must be able to accept regenerated current. Do not use a bench supply that cannot sink current unless a separate braking/dump path is installed.

## Measurements required

At >=100 Hz if possible:
- rotor RPM
- DC bus voltage
- DC bus current
- motor phase current if available
- controller temperature
- motor temperature
- frame vibration

## Energy accounting

Input energy:
    E_in = integral(V_bus * I_bus dt) during acceleration

Recovered energy:
    E_out = -integral(V_bus * I_bus dt) during regenerative deceleration

Round-trip bench efficiency:
    eta = E_out / E_in

This includes motor, controller, bearing, windage, coupling, and wiring losses for the complete test article.
