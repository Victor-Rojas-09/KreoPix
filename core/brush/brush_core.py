import math
from dataclasses import dataclass
from services.brushes.brush_cache import BrushCache
from services.brushes.brush_engine import BrushEngine

@dataclass
class BrushPoint:
    """Represents a point in a brush stroke with pressure sensitivity."""

    x: float
    y: float
    pressure: float = 1.0


def interpolate(p1: BrushPoint, p2: BrushPoint, spacing: float):
    """Generate interpolated points between two BrushPoints based on spacing."""

    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        yield p1
        return

    step = spacing / dist
    t = 0.0

    while t <= 1.0:
        yield BrushPoint(
            x=p1.x + dx * t,
            y=p1.y + dy * t,
            pressure=p1.pressure + (p2.pressure - p1.pressure) * t
        )
        t += step


class BaseBrushType:
    """Defines base behavior for a brush, including size and opacity handling."""

    def __init__(self, size=50, opacity=100, soft=True):
        self.base_size = size
        self.base_opacity = opacity
        self.soft = soft

    def get_size(self, point: BrushPoint):
        """Calculate brush size based on pressure."""
        return max(1, int(self.base_size * point.pressure))

    def get_opacity(self, point: BrushPoint):
        """Calculate brush opacity based on pressure."""
        return (self.base_opacity / 100.0) * point.pressure

    def apply(self, engine: BrushEngine, point: BrushPoint, color):
        """Apply the brush stamp to the engine at a given point."""

        size = self.get_size(point)
        opacity = self.get_opacity(point)
        mask = BrushCache.get_mask(size, self.soft)
        engine.apply_stamp(
            mask=mask,
            color=color,
            x=point.x,
            y=point.y,
            opacity=opacity
        )


class Brush:
    """Handles brush stroke application using interpolation and a brush engine."""

    def __init__(self, brush_type: BaseBrushType, engine: BrushEngine, spacing=3):
        self.brush_type = brush_type
        self.engine = engine
        self.spacing = spacing

    def apply_stroke(self, layer, points, color=None):
        """Apply a continuous stroke across a sequence of points."""

        if not points or len(points) < 2:
            return

        color = color or (0, 0, 0, 255)
        self.engine.begin_stroke(layer)

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            for p in interpolate(p1, p2, self.spacing):
                self.brush_type.apply(self.engine, p, color)

        self.engine.end_stroke(layer)


class BrushFactory:
    """Factory class to create configured Brush instances based on type."""

    @staticmethod
    def create(brush_type):
        """Create a Brush with appropriate spacing based on its type."""

        engine = BrushEngine()
        spacing = 3
        name = getattr(brush_type, "name", "")

        if name == "airbrush":
            spacing = 2
        elif name == "hard":
            spacing = 5
        elif name == "eraser":
            spacing = 4

        return Brush(brush_type=brush_type, engine=engine, spacing=spacing)