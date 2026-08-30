from dataclasses import dataclass


BATTERY_MAX_V = 29.2
FUSE_MAX_A = 10.0
COMMISSIONING_MAX_A = 5.0
DUMP_OHMS = 22.0
DUMP_MIN_W = 100.0
OVERSPEED_RPM = 1650.0
RPM_FEATURES = 12


@dataclass(frozen=True)
class SafetyPart:
    kind: str
    voltage_v: float = 0.0
    current_a: float = 0.0
    nc_contacts: int = 0
    latching: bool = False
    resistance_ohm: float = 0.0
    power_w: float = 0.0
    response_us: float = 0.0


def overspeed_pulse_hz() -> float:
    return OVERSPEED_RPM / 60.0 * RPM_FEATURES


def validate_safety_part(part: SafetyPart) -> list[str]:
    """Fail-closed minimum P1 substitution checks for safety-critical purchased parts."""
    errors: list[str] = []
    if part.kind == "fuse_holder":
        if part.voltage_v < 32.0:
            errors.append("fuse holder must be rated >=32 VDC")
        if part.current_a < FUSE_MAX_A:
            errors.append("fuse holder must be rated >=10 A")
    elif part.kind == "fuse":
        if part.voltage_v < 32.0:
            errors.append("fuse must be rated >=32 VDC")
        if part.current_a != FUSE_MAX_A:
            errors.append("P1 fuse must be exactly 10 A")
    elif part.kind == "k1":
        if part.voltage_v < 32.0:
            errors.append("K1 contacts must be rated >=32 VDC")
        if part.current_a < FUSE_MAX_A:
            errors.append("K1 contacts must be rated >=10 A")
    elif part.kind == "estop":
        if part.nc_contacts < 1:
            errors.append("E-stop requires at least one NC contact")
        if not part.latching:
            errors.append("E-stop must latch until deliberate reset")
    elif part.kind == "dump":
        if abs(part.resistance_ohm - DUMP_OHMS) > 0.5:
            errors.append("dump resistor must be 22 ohm class")
        if part.power_w < DUMP_MIN_W:
            errors.append("dump resistor must be rated >=100 W")
    elif part.kind == "rpm_sensor":
        # At 1650 rpm and 12 features: 330 Hz, 3.03 ms full period.
        # Require <=250 us response for comfortable edge timing margin.
        if part.response_us <= 0 or part.response_us > 250.0:
            errors.append("RPM sensor response must be <=250 us")
    else:
        errors.append(f"unknown safety part kind: {part.kind}")
    return errors
