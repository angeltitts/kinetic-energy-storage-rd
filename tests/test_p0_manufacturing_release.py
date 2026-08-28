import math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"prototype"/"p0"))
from digital_twin import P0DigitalTwin, AnnularRotor

def test_release_energy_limit():
    twin=P0DigitalTwin()
    assert twin.total_rotor_energy_at_300rpm_j < 2.0

def test_release_ring_masses():
    masses=[
        AnnularRotor(0.300,0.270,0.006).mass_kg,
        AnnularRotor(0.240,0.210,0.006).mass_kg,
        AnnularRotor(0.180,0.150,0.006).mass_kg,
    ]
    assert all(m<0.11 for m in masses)
    assert masses[0]>masses[1]>masses[2]

def test_10min_virtual_tracking():
    twin=P0DigitalTwin()
    twin.run_constant((180,120,60),600.0,dt=0.02)
    for measured,target in zip(twin.rpms,(180,120,60)):
        assert abs(measured-target)/target < 0.05
