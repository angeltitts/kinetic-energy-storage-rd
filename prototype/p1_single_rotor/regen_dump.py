from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PassiveDump:
    resistance_ohm: float = 22.0
    rated_power_w: float = 100.0

    def current_a(self, bus_voltage_v: float) -> float:
        if bus_voltage_v < 0:
            raise ValueError("bus_voltage_v must be non-negative")
        return bus_voltage_v / self.resistance_ohm

    def power_w(self, bus_voltage_v: float) -> float:
        return bus_voltage_v**2 / self.resistance_ohm

    def absorbs_regen_without_battery_charge(
        self,
        bus_voltage_v: float,
        regen_current_limit_a: float,
    ) -> bool:
        if regen_current_limit_a < 0:
            raise ValueError("regen_current_limit_a must be non-negative")
        return self.current_a(bus_voltage_v) >= regen_current_limit_a

    def power_fraction(self, bus_voltage_v: float) -> float:
        return self.power_w(bus_voltage_v) / self.rated_power_w


P1_REGEN_CURRENT_LIMIT_A = 1.0
P1_REGEN_ENABLE_MIN_BUS_V = 24.0
P1_REGEN_ENABLE_MAX_BUS_V = 28.0


def validate_p1_dump(dump: PassiveDump = PassiveDump()) -> dict[str, float | bool]:
    p_min = dump.power_w(P1_REGEN_ENABLE_MIN_BUS_V)
    p_max = dump.power_w(P1_REGEN_ENABLE_MAX_BUS_V)
    return {
        "dump_current_at_24v_a": dump.current_a(24.0),
        "dump_power_at_24v_w": p_min,
        "dump_power_at_28v_w": p_max,
        "dump_power_at_29p2v_w": dump.power_w(29.2),
        "absorbs_1a_at_24v": dump.absorbs_regen_without_battery_charge(
            24.0, P1_REGEN_CURRENT_LIMIT_A
        ),
        "max_window_power_fraction": p_max / dump.rated_power_w,
    }
