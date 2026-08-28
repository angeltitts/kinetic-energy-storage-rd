from dataclasses import dataclass
import math

AL6061_DENSITY = 2700.0

@dataclass(frozen=True)
class SolidDiskRotor:
    diameter_m: float = 0.200
    thickness_m: float = 0.006
    density_kg_m3: float = AL6061_DENSITY

    @property
    def radius_m(self):
        return self.diameter_m / 2

    @property
    def mass_kg(self):
        return math.pi * self.radius_m**2 * self.thickness_m * self.density_kg_m3

    @property
    def inertia_kg_m2(self):
        return 0.5 * self.mass_kg * self.radius_m**2

    def energy_j(self, rpm):
        omega = rpm * 2 * math.pi / 60
        return 0.5 * self.inertia_kg_m2 * omega**2

    def rim_speed_m_s(self, rpm):
        return rpm * 2 * math.pi / 60 * self.radius_m

@dataclass(frozen=True)
class P1Limits:
    command_rpm: float = 1500.0
    overspeed_rpm: float = 1650.0
    max_allowed_energy_j: float = 40.0

def evaluate(rotor=SolidDiskRotor(), limits=P1Limits()):
    return {
        "mass_kg": rotor.mass_kg,
        "inertia_kg_m2": rotor.inertia_kg_m2,
        "energy_at_command_j": rotor.energy_j(limits.command_rpm),
        "energy_at_overspeed_j": rotor.energy_j(limits.overspeed_rpm),
        "rim_speed_at_command_m_s": rotor.rim_speed_m_s(limits.command_rpm),
        "passes_energy_limit": rotor.energy_j(limits.overspeed_rpm) <= limits.max_allowed_energy_j,
    }

if __name__ == "__main__":
    for key, value in evaluate().items():
        print(f"{key}: {value}")
