import numpy as np
from PIL import Image


class BrushEngine:
    """Handles low-level brush rendering using an off-screen buffer."""

    def __init__(self):
        self.buffer = None
        self._target_layer = None

    def begin_stroke(self, layer: Image.Image):
        """Start a new stroke by creating a transparent buffer matching the layer size."""

        self._target_layer = layer
        self.buffer = Image.new("RGBA", layer.size, (0, 0, 0, 0))

    def end_stroke(self, layer: Image.Image):
        """Finalize the stroke by compositing the buffer onto the target layer."""

        if self.buffer:
            layer.alpha_composite(self.buffer)
        self.buffer = None
        self._target_layer = None

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
        """Reduce alpha under the mask (destination stays RGB; only A scales down)."""

        if self._target_layer is None:
            return

        size = mask.size[0]
        half = size // 2
        bx0, by0 = int(x - half), int(y - half)
        bw, bh = self._target_layer.size

        ix0 = max(0, bx0)
        iy0 = max(0, by0)
        ix1 = min(bw, bx0 + size)
        iy1 = min(bh, by0 + size)
        if ix0 >= ix1 or iy0 >= iy1:
            return

        mx0 = ix0 - bx0
        my0 = iy0 - by0
        mx1 = mx0 + (ix1 - ix0)
        my1 = my0 + (iy1 - iy0)

        m = np.asarray(mask.crop((mx0, my0, mx1, my1)).convert("L"), dtype=np.float32) / 255.0
        f = np.clip(1.0 - m * float(strength), 0.0, 1.0)
        buf = np.array(self._target_layer)
        sub = buf[iy0:iy1, ix0:ix1, :]
        sub[..., 3] = np.clip(sub[..., 3].astype(np.float32) * f, 0, 255).astype(np.uint8)
        updated_layer = Image.fromarray(buf, "RGBA")
        self._target_layer.paste(updated_layer)