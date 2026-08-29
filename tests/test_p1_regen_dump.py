import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "prototype" / "p1_single_rotor"))

from regen_dump import (
    P1_REGEN_CURRENT_LIMIT_A,
    P1_REGEN_ENABLE_MAX_BUS_V,
    P1_REGEN_ENABLE_MIN_BUS_V,
    PassiveDump,
    validate_p1_dump,
)


def test_22_ohm_dump_exceeds_one_amp_at_24v():
    dump = PassiveDump()
    assert dump.current_a(P1_REGEN_ENABLE_MIN_BUS_V) > P1_REGEN_CURRENT_LIMIT_A
    assert dump.absorbs_regen_without_battery_charge(24.0, 1.0)


def test_dump_power_has_large_margin_in_released_regen_window():
    dump = PassiveDump()
    assert dump.power_w(P1_REGEN_ENABLE_MAX_BUS_V) < 40.0
    assert dump.power_fraction(P1_REGEN_ENABLE_MAX_BUS_V) < 0.40


def test_dump_still_below_half_rating_at_29p2v_charge_ceiling():
    dump = PassiveDump()
    assert dump.power_w(29.2) < 40.0
    assert dump.power_fraction(29.2) < 0.40


def test_reference_values():
    result = validate_p1_dump()
    assert math.isclose(result["dump_current_at_24v_a"], 24.0 / 22.0, rel_tol=1e-12)
    assert result["absorbs_1a_at_24v"] is True


def test_invalid_inputs_rejected():
    dump = PassiveDump()
    try:
        dump.current_a(-1.0)
        assert False
    except ValueError:
        pass
    try:
        dump.absorbs_regen_without_battery_charge(24.0, -1.0)
        assert False
    except ValueError:
        pass
