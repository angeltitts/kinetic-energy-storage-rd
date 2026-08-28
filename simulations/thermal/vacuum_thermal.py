from __future__ import annotations

from dataclasses import dataclass
import math

STEFAN_BOLTZMANN = 5.670374419e-8


@dataclass
class VacuumThermalModel:
    liner_density_kg_m3: float = 2500.0
    liner_specific_heat_j_kg_k: float = 900.0
    initial_temperature_k: float = 300.0
    liner_area_m2: float = 0.10

    @staticmethod
    def radiated_power(t_hub: float, t_shell: float, emissivity: float, area: float) -> float:
        if min(t_hub, t_shell, area) < 0:
            raise ValueError("temperatures and area must be non-negative")
        if not 0 <= emissivity <= 1:
            raise ValueError("emissivity must be between 0 and 1")
        return emissivity * STEFAN_BOLTZMANN * area * (t_hub**4 - t_shell**4)

    def simulate_ablative_braking_event(
        self,
        rotor_kinetic_energy_joules: float,
        ablative_mass_kg: float,
        latent_heat_sublimation: float,
        sensible_temperature_limit_k: float = 1800.0,
    ) -> dict:
        """Reduced energy-balance screen for a sacrificial liner."""
        if rotor_kinetic_energy_joules < 0 or ablative_mass_kg <= 0 or latent_heat_sublimation <= 0:
            raise ValueError("energy must be non-negative; mass and latent heat must be positive")
        if sensible_temperature_limit_k <= self.initial_temperature_k:
            raise ValueError("temperature limit must exceed initial temperature")

        sensible_capacity = ablative_mass_kg * self.liner_specific_heat_j_kg_k * (
            sensible_temperature_limit_k - self.initial_temperature_k
        )
        sensible_used = min(rotor_kinetic_energy_joules, sensible_capacity)
        remaining = max(0.0, rotor_kinetic_energy_joules - sensible_used)
        ablated_mass = min(ablative_mass_kg, remaining / latent_heat_sublimation)
        if sensible_used < sensible_capacity:
            final_temp = self.initial_temperature_k + sensible_used / (
                ablative_mass_kg * self.liner_specific_heat_j_kg_k
            )
        else:
            final_temp = sensible_temperature_limit_k

        volume_lost = ablated_mass / self.liner_density_kg_m3
        ablation_depth = volume_lost / self.liner_area_m2 if self.liner_area_m2 > 0 else math.inf
        residual_energy = max(0.0, remaining - ablated_mass * latent_heat_sublimation)
        return {
            "final_temperature_k": final_temp,
            "sensible_energy_j": sensible_used,
            "ablated_mass_kg": ablated_mass,
            "ablation_depth_m": ablation_depth,
            "residual_unabsorbed_energy_j": residual_energy,
            "fully_absorbed": residual_energy <= 1e-9,
        }
