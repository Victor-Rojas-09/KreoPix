import math
from dataclasses import dataclass


@dataclass
class BrushPoint:
    """Represents a point in a brush stroke."""

    x: int
    y: int
    pressure: float = 1.0


def interpolate(p1: BrushPoint, p2: BrushPoint, spacing: float):
    """Generate interpolated points between two points."""

    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist = math.hypot(dx, dy)

    steps = max(1, int(dist / spacing))

    for i in range(steps + 1):
        t = i / steps
        yield BrushPoint(
            x=int(p1.x + dx * t),
            y=int(p1.y + dy * t),
            pressure=p1.pressure + (p2.pressure - p1.pressure) * t
        )