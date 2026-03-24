from PIL import Image

class BrushEngine:
    """Handles low-level brush rendering using an off-screen buffer."""

    def __init__(self):
        """Initialize the brush engine with an empty buffer."""
        self.buffer = None

    def begin_stroke(self, layer: Image.Image):
        """Start a new stroke by creating a transparent buffer matching the layer size."""
        self.buffer = Image.new("RGBA", layer.size, (0, 0, 0, 0))

    def end_stroke(self, layer: Image.Image):
        """Finalize the stroke by compositing the buffer onto the target layer."""
        if self.buffer:
            layer.alpha_composite(self.buffer)
            self.buffer = None

    def apply_stamp(self, mask, color, x, y, opacity):
        """Apply a brush stamp onto the buffer at the given position."""

        if self.buffer is None:
            return

        size = mask.size[0]
        half = size // 2
        r, g, b = color[:3]

        # Create stamp with alpha derived from mask and opacity
        alpha = mask.point(lambda a: int(a * opacity))
        stamp = Image.new("RGBA", (size, size), (r, g, b, 0))
        stamp.putalpha(alpha)

        self.buffer.paste(
            stamp,
            (int(x - half), int(y - half)),
            stamp
        )

    def apply_eraser(self, mask, x, y, strength):
        """Apply an erasing effect by reducing alpha in the buffer."""

        if self.buffer is None:
            return

        size = mask.size[0]
        half = size // 2

        alpha = mask.point(lambda a: int(a * strength))

        erase_layer = Image.new("RGBA", self.buffer.size, (0, 0, 0, 0))
        erase_layer.paste(
            Image.merge("RGBA", (alpha, alpha, alpha, alpha)),
            (int(x - half), int(y - half)),
            alpha
        )

        self.buffer = Image.alpha_composite(self.buffer, erase_layer)