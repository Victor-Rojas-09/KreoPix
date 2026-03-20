from services.brushes.brush import Brush
from services.brushes.brush_tip import BrushTip
from services.brushes.brush_dynamics import BrushDynamics
from services.brushes.brush_renderer import BrushRenderer


def create_airbrush(color):
    """Soft brush with opacity buildup."""

    return Brush(
        tip=BrushTip("soft", color),
        dynamics=BrushDynamics(size=80, opacity=30, spacing=3),
        renderer=BrushRenderer("accumulate")
    )


def create_hard_brush(color):
    """Solid brush with consistent opacity."""

    return Brush(
        tip=BrushTip("hard", color),
        dynamics=BrushDynamics(size=50, opacity=100, spacing=5),
        renderer=BrushRenderer("normal")
    )


def create_eraser():
    """Soft eraser that removes transparency."""

    return Brush(
        tip=BrushTip("soft", (0, 0, 0, 255)),
        dynamics=BrushDynamics(size=60, opacity=100, spacing=4),
        renderer=BrushRenderer("erase")
    )