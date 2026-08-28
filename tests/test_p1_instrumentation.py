import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from instrumentation import (
    Sample,
    coastdown_loss_power_w,
    integrate_bus_energy_j,
    kinetic_energy_j,
    round_trip_efficiency,
)


def test_bus_energy_trapezoid():
    samples = [
        Sample(0.0, 0, 24.0, 1.0),
        Sample(2.0, 0, 24.0, 1.0),
    ]
    assert math.isclose(integrate_bus_energy_j(samples), 48.0, rel_tol=1e-12)


def test_regen_efficiency_sign_convention():
    charge = [
        Sample(0.0, 0, 20.0, 1.0),
        Sample(10.0, 0, 20.0, 1.0),
    ]
    regen = [
        Sample(0.0, 0, 20.0, -0.8),
        Sample(10.0, 0, 20.0, -0.8),
    ]
    assert math.isclose(round_trip_efficiency(charge, regen), 0.8, rel_tol=1e-12)


def test_reference_kinetic_energy():
    inertia = 0.0025446900
    assert 31.0 < kinetic_energy_j(inertia, 1500.0) < 32.0


def test_coastdown_loss_is_positive():
    p = coastdown_loss_power_w(0.0025446900, 1500, 300, 60)
    assert p > 0
