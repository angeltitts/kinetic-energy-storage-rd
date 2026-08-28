from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import time


@dataclass
class TelemetryFrame:
    timestamp_s: float
    ring_rpm: list[float]
    bearing_temperature_k: float
    shell_pressure_torr: float
    vibration_g: float
    fault: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"))


class TelemetryLogger:
    def __init__(self) -> None:
        self.frames: list[TelemetryFrame] = []

    def add(self, ring_rpm, bearing_temperature_k, shell_pressure_torr, vibration_g, fault="") -> TelemetryFrame:
        frame = TelemetryFrame(
            time.time(),
            list(map(float, ring_rpm)),
            float(bearing_temperature_k),
            float(shell_pressure_torr),
            float(vibration_g),
            str(fault),
        )
        self.frames.append(frame)
        return frame
