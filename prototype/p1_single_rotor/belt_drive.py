from __future__ import annotations
import math

PITCH_MM = 5.0
MOTOR_TEETH = 15
SHAFT_TEETH = 48
BELT_TEETH = 80

def pitch_diameter_mm(teeth: int) -> float:
    return teeth * PITCH_MM / math.pi

def belt_length_mm(center_distance_mm: float) -> float:
    d1 = pitch_diameter_mm(MOTOR_TEETH)
    d2 = pitch_diameter_mm(SHAFT_TEETH)
    c = center_distance_mm
    return 2*c + math.pi/2*(d1+d2) + (d2-d1)**2/(4*c)

def center_distance_for_belt(target_length_mm: float = BELT_TEETH * PITCH_MM) -> float:
    lo, hi = 20.0, 300.0
    for _ in range(100):
        mid = (lo+hi)/2
        if belt_length_mm(mid) < target_length_mm:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

def rotor_rpm_from_motor(motor_rpm: float) -> float:
    return motor_rpm * MOTOR_TEETH / SHAFT_TEETH

def motor_rpm_from_voltage(voltage_v: float, kv_rpm_per_v: float = 200.0) -> float:
    return voltage_v * kv_rpm_per_v

if __name__ == "__main__":
    c = center_distance_for_belt()
    motor = motor_rpm_from_voltage(25.6)
    rotor = rotor_rpm_from_motor(motor)
    print(f"Nominal center distance: {c:.3f} mm")
    print(f"Motor no-load estimate at 25.6 V: {motor:.0f} RPM")
    print(f"Ideal rotor speed through 15:48 drive: {rotor:.0f} RPM")
