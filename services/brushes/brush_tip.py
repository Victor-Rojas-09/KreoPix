from services.brushes.brush_utils import BrushUtils


class BrushTip:
    """Defines the shape of the brush (soft or hard)."""

    def __init__(self, shape="soft", color=(0, 0, 0, 255)):
        self.shape = shape
        self.color = color
        self._cache = {}

    def get_stamp(self, size: int, opacity: float):
        """Returns a cached brush image."""

        key = (size, int(opacity))

        if key not in self._cache:
            if self.shape == "soft":
                brush = BrushUtils.create_soft_brush(size, self.color, opacity)
            else:
                brush = BrushUtils.create_hard_brush(size, self.color, opacity)

            self._cache[key] = brush

        return self._cache[key]