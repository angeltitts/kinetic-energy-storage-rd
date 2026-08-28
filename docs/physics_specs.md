# Gen-4.1 CSRC Physics Specifications

This implementation is a screening and prototype-support codebase for a concentric slip-ring kinetic energy storage concept.

## Governing relations

For a thin hoop, the ideal rotor specific-energy relation is

\[ e = \frac{\sigma}{2\rho} \]

and the corresponding material-limited tip speed is

\[ v = \sqrt{\frac{\sigma}{\rho}}. \]

The project keeps a nominal inter-ring radial gap of 0.5 mm and treats the internal gas pressure as a parameter from 1e-2 to 1e-5 Torr.

## Scope

The simulations are deliberately reduced-order. They are intended to expose design sensitivities and failure of assumptions before high-fidelity FEA/CFD/rotordynamic work. They do not validate high-energy hardware.
