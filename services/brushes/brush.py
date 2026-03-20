from services.brushes.stroke import interpolate


class Brush:
    """High-level brush class. Coordinates stroke interpolation,
    dynamics (size and opacity), tip shape, and brush rendering."""

    def __init__(self, tip, dynamics, renderer):
        self.tip = tip
        self.dynamics = dynamics
        self.renderer = renderer

    def apply_stroke(self, layer, points):
        """Apply a full stroke to the layer."""

        if not points:
            return

        self.renderer.begin(layer)

        spacing = self.dynamics.get_spacing()

        for i in range(len(points) - 1):
            for p in interpolate(points[i], points[i + 1], spacing):
                size = self.dynamics.get_size(p)
                opacity = self.dynamics.get_opacity(p)

                stamp = self.tip.get_stamp(size, opacity)
                self.renderer.apply(layer, stamp, p.x, p.y)

        self.renderer.end(layer)