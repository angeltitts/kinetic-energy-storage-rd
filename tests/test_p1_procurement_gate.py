from prototype.p1_single_rotor.procurement_gate import SafetyPart, overspeed_pulse_hz, validate_safety_part


def test_released_primary_parts_pass():
    parts = [
        SafetyPart(kind="fuse_holder", voltage_v=32, current_a=30),
        SafetyPart(kind="fuse", voltage_v=32, current_a=10),
        SafetyPart(kind="k1", voltage_v=75, current_a=20),
        SafetyPart(kind="estop", nc_contacts=1, latching=True),
        SafetyPart(kind="dump", resistance_ohm=22, power_w=100),
        SafetyPart(kind="rpm_sensor", response_us=4),
    ]
    assert all(validate_safety_part(part) == [] for part in parts)


def test_overspeed_pulse_rate_is_330_hz():
    assert overspeed_pulse_hz() == 330.0


def test_underrated_k1_rejected():
    errors = validate_safety_part(SafetyPart(kind="k1", voltage_v=28, current_a=20))
    assert errors


def test_non_latching_estop_rejected():
    errors = validate_safety_part(SafetyPart(kind="estop", nc_contacts=1, latching=False))
    assert errors


def test_wrong_fuse_rejected():
    errors = validate_safety_part(SafetyPart(kind="fuse", voltage_v=32, current_a=15))
    assert errors


def test_slow_rpm_sensor_rejected():
    errors = validate_safety_part(SafetyPart(kind="rpm_sensor", response_us=1000))
    assert errors
