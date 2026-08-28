import math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"prototype"/"p1_single_rotor"))
from belt_drive import center_distance_for_belt, rotor_rpm_from_motor, motor_rpm_from_voltage

def test_center_distance():
    assert math.isclose(center_distance_for_belt(),118.336,abs_tol=0.01)

def test_drive_ratio():
    assert math.isclose(rotor_rpm_from_motor(4800),1500,rel_tol=1e-12)

def test_nominal_25p6v_does_not_require_overdrive():
    motor=motor_rpm_from_voltage(25.6)
    assert rotor_rpm_from_motor(motor) > 1500
    assert rotor_rpm_from_motor(motor) < 1650
