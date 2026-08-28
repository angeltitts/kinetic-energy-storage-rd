import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulations.rotordynamics.whirl_model import RotorDynamicsModel
from simulations.gas_shear.shear_coupling import InterRingShearModel
from simulations.thermal.vacuum_thermal import VacuumThermalModel
from embedded.emergency_brake import BrakeLimits, EmergencyBrakeController


def test_rotordynamics_and_plot(tmp_path):
    model = RotorDynamicsModel(0.30, 0.002, 1800.0, 230.0, 2e6, 3e6)
    result = model.calculate_critical_speeds(150000)
    assert result["rpm"][-1] == 150000
    out = model.plot_campbell_diagram(tmp_path / "campbell.png")
    assert out.exists() and out.stat().st_size > 1000


def test_knudsen_regime_and_torque_solution():
    model = InterRingShearModel(3, pressure_torr=1e-3, gas_species="helium")
    kn = model.compute_knudsen_number()
    assert kn["knudsen_number"] > 0
    t = np.linspace(0, 5, 101)
    result = model.torque_transfer(1000, t)
    assert result["ring_rpm"].shape == (3, len(t))
    assert model.get_acceleration_lag() >= 0


def test_radiation_and_ablative_balance():
    thermal = VacuumThermalModel()
    power = thermal.radiated_power(400, 300, 0.8, 0.2)
    assert power > 0
    result = thermal.simulate_ablative_braking_event(1e4, 0.5, 3e6)
    assert result["ablated_mass_kg"] >= 0
    assert result["residual_unabsorbed_energy_j"] >= 0


def test_emergency_brake_latches():
    ctl = EmergencyBrakeController(BrakeLimits(330, 1.0, 360, 1e-2))
    assert ctl.evaluate([100, 340, 100], 0.1, 300, 1e-4)
    assert ctl.reason == "overspeed"
    ctl.reset()
    assert not ctl.latched
