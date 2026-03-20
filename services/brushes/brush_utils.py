import math
from PIL import Image


class BrushUtils:
    """Utility class for generating brush tip images."""

    @staticmethod
    def create_soft_brush(size: int, color: tuple, opacity: float) -> Image:
        """Create a soft circular brush with smooth radial falloff."""

        radius = size // 2
        r, g, b, _ = color
        opacity = max(0.0, min(1.0, opacity / 100.0))

        brush = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        pixels = brush.load()

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= radius:
                    # Smooth falloff curve (tweak exponent for softness)
                    falloff = (1 - (dist / radius)) ** 4.0

                    alpha = int(255 * opacity * falloff)

                    # Premultiplied alpha (important!)
                    pr = int(r * (alpha / 255))
                    pg = int(g * (alpha / 255))
                    pb = int(b * (alpha / 255))

                    pixels[x, y] = (pr, pg, pb, alpha)

        return brush

    @staticmethod
    def create_hard_brush(size: int, color: tuple, opacity: float) -> Image:
        """Create a hard circular brush with no falloff."""

        radius = size // 2
        r, g, b, _ = color
        alpha = int(255 * max(0.0, min(1.0, opacity / 100.0)))

        brush = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        pixels = brush.load()

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius

                if dx * dx + dy * dy <= radius * radius:
                    pixels[x, y] = (r, g, b, alpha)

        return brush

    @staticmethod
    def create_alpha_brush(size: int, opacity: float, soft: bool = True) -> Image:
        """Create a brush that only contains alpha information."""

        radius = size // 2
        opacity = max(0.0, min(1.0, opacity / 100.0))

        brush = Image.new("L", (size, size), 0)
        pixels = brush.load()

        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius
                dist = math.sqrt(dx * dx + dy * dy)

                if dist <= radius:
                    if soft:
                        falloff = (1 - (dist / radius)) ** 4.0
                    else:
                        falloff = 1.0

                    alpha = int(255 * opacity * falloff)
                    pixels[x, y] = alpha

        return brush