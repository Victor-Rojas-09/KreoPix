from core.brush.brush_core import BaseBrushType, BrushFactory

class AirbrushType(BaseBrushType):
    """Soft brush with low opacity for smooth, airbrush like effects."""

    name = "airbrush"

    def __init__(self, size=80, opacity=30):
        """Initialize airbrush with larger size and lower opacity."""

        super().__init__(size=size, opacity=opacity, soft=True)

    def get_opacity(self, point):
        """Reduce opacity further for a softer spray effect."""

        return super().get_opacity(point) * 0.5


class HardBrushType(BaseBrushType):
    """Hard-edged brush with full opacity, ignoring pressure variation."""

    name = "hard"

    def __init__(self, size=50, opacity=100):
        """Initialize hard brush with sharp edges."""

        super().__init__(size=size, opacity=opacity, soft=False)

    def get_opacity(self, point):
        """Return constant opacity, ignoring pressure."""

        return self.base_opacity / 100.0


class EraserType(BaseBrushType):
    """Soft brush used for erasing content."""

    name = "eraser"

    def __init__(self, size=60, opacity=100):
        """Initialize eraser with full opacity and soft edges."""
        super().__init__(size=size, opacity=opacity, soft=True)


def create_airbrush(color):
    """Create a brush instance configured as an airbrush."""
    return BrushFactory.create(AirbrushType())


def create_hard_brush(color):
    """Create a brush instance configured as a hard brush."""
    return BrushFactory.create(HardBrushType())


def create_eraser():
    """Create a brush instance configured as an eraser."""
    return BrushFactory.create(EraserType())