from PIL import Image
import math

class BrushUtils:
    """Utility class for generating brush masks."""

    @staticmethod
    def create_soft_mask(size: int) -> Image:
        """Create a circular soft mask with smooth falloff towards the edges."""

        radius = size / 2.0
        mask = Image.new("L", (size, size), 0)
        pixels = mask.load()

        for y in range(size):
            for x in range(size):
                dx = x + 0.5 - radius
                dy = y + 0.5 - radius
                dist = math.hypot(dx, dy)

                if dist <= radius:
                    falloff = (1 - (dist / radius)) ** 2.0
                    pixels[x, y] = int(255 * falloff)

        return mask

    @staticmethod
    def create_hard_mask(size: int) -> Image:
        """Create a circular hard mask with solid edges (no falloff)."""

        radius = size / 2.0
        mask = Image.new("L", (size, size), 0)
        pixels = mask.load()

        for y in range(size):
            for x in range(size):
                dx = x + 0.5 - radius
                dy = y + 0.5 - radius

                if dx * dx + dy * dy <= radius * radius:
                    pixels[x, y] = 255

        return mask