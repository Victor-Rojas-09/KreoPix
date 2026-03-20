import math
from PIL import Image


class BrushUtils:
    """Utility methods shared across multiple brush implementations."""

    @staticmethod
    def interpolate(p1, p2, step=2):
        """
        Generate interpolated points between two coordinates.

        Args:
            p1 (tuple): Starting point (x, y)
            p2 (tuple): Ending point (x, y)
            step (int): Distance between generated points

        Yields:
            tuple: Interpolated (x, y) coordinates
        """
        x1, y1 = p1
        x2, y2 = p2

        dist = math.hypot(x2 - x1, y2 - y1)
        steps = max(1, int(dist / step))

        for i in range(steps):
            t = i / steps
            yield int(x1 + (x2 - x1) * t), int(y1 + (y2 - y1) * t)

    @staticmethod
    def create_soft_brush(size, color, opacity):
        """
        Create a circular soft brush with radial falloff.

        Uses premultiplied alpha to avoid compositing artifacts.

        Args:
            size (int): Diameter of the brush
            color (tuple): RGBA color
            opacity (int): Opacity percentage (0–100)

        Returns:
            PIL.Image: Soft brush image
        """
        radius = size // 2
        r, g, b, _ = color
        opacity = opacity / 100

        brush = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        pixels = brush.load()

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= radius:
                    falloff = (1 - (dist / radius)) ** 4.4
                    alpha = int(255 * opacity * falloff)

                    # Premultiplied color
                    pr = int(r * (alpha / 255))
                    pg = int(g * (alpha / 255))
                    pb = int(b * (alpha / 255))

                    pixels[x, y] = (pr, pg, pb, alpha)

        return brush

    @staticmethod
    def create_hard_brush(size, color, opacity):
        """
        Create a solid circular brush (no falloff).

        Args:
            size (int): Diameter of the brush
            color (tuple): RGBA color
            opacity (int): Opacity percentage (0–100)

        Returns:
            PIL.Image: Hard brush image
        """
        radius = size // 2
        r, g, b, _ = color
        alpha = int(255 * (opacity / 100))

        brush = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        pixels = brush.load()

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius

                if dx * dx + dy * dy <= radius * radius:
                    pixels[x, y] = (r, g, b, alpha)

        return brush