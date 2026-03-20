class BrushDynamics:
    """Controls how brush properties change during painting."""

    def __init__(self, size=50, opacity=100, spacing=5):
        self.base_size = size
        self.base_opacity = opacity
        self.spacing = spacing

    def get_size(self, point):
        """Size affected by pressure."""

        return max(1, int(self.base_size * point.pressure))

    def get_opacity(self, point):
        """Opacity affected by pressure."""

        return self.base_opacity * point.pressure

    def get_spacing(self):
        """Spacing affected by pressure."""

        return self.spacing