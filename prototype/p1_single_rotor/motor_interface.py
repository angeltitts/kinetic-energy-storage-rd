from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MotorFaceMeasurement:
    bolt_count: int
    bolt_circle_mm: float
    hole_diameter_mm: float
    center_clearance_mm: float

    def validate(self) -> None:
        if self.bolt_count < 3:
            raise ValueError("bolt_count must be >= 3")
        if self.bolt_circle_mm <= 0 or self.hole_diameter_mm <= 0:
            raise ValueError("measured dimensions must be positive")
        if self.center_clearance_mm <= 0:
            raise ValueError("center_clearance_mm must be positive")
        if self.center_clearance_mm + self.hole_diameter_mm >= self.bolt_circle_mm:
            raise ValueError("center clearance overlaps motor mounting holes")

    def hole_centers_mm(self) -> list[tuple[float, float]]:
        self.validate()
        radius = self.bolt_circle_mm / 2.0
        return [
            (
                radius * math.cos(2.0 * math.pi * i / self.bolt_count),
                radius * math.sin(2.0 * math.pi * i / self.bolt_count),
            )
            for i in range(self.bolt_count)
        ]


def required_plate_margin_mm(
    measurement: MotorFaceMeasurement,
    plate_width_mm: float = 90.0,
    minimum_edge_margin_mm: float = 8.0,
) -> float:
    """Return remaining radial edge margin around the motor-hole pattern.

    Positive means the measured mounting pattern fits the released 90 mm plate width
    with the requested minimum edge margin. Negative means the plate must be widened.
    """
    measurement.validate()
    outer_hole_radius = measurement.bolt_circle_mm / 2.0 + measurement.hole_diameter_mm / 2.0
    available_radius = plate_width_mm / 2.0 - minimum_edge_margin_mm
    return available_radius - outer_hole_radius
