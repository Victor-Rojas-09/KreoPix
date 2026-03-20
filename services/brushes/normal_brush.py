from PIL import Image
from services.brushes.base_brush import BaseBrush
from services.brushes.brush_utils import BrushUtils


class NormalBrush(BaseBrush):
    """
    Solid brush with uniform opacity.

    This brush paints with consistent color and opacity,
    without accumulation effects.

    Characteristics:
    - Hard edges
    - No opacity buildup
    - Predictable strokes
    """

    def apply_stroke(self, layer_image, points):
        if not points:
            return

        if layer_image.mode != "RGBA":
            layer_image = layer_image.convert("RGBA")

        brush = BrushUtils.create_hard_brush(self.size, self.color, self.opacity)
        half = self.size // 2

        for i in range(len(points) - 1):
            for x, y in BrushUtils.interpolate(points[i], points[i + 1]):
                layer_image.paste(brush, (x - half, y - half), brush)

        x, y = points[-1]
        layer_image.paste(brush, (x - half, y - half), brush)