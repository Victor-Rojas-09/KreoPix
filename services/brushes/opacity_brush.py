from PIL import Image
from services.brushes.base_brush import BaseBrush
from services.brushes.brush_utils import BrushUtils


class OpacityBrush(BaseBrush):
    """
    Soft brush with opacity buildup (airbrush behavior).

    This brush uses radial falloff and premultiplied alpha.
    Multiple passes accumulate opacity gradually, similar to an airbrush.

    Characteristics:
    - Soft edges
    - Opacity buildup
    - Smooth blending
    """

    def apply_stroke(self, layer_image, points):
        if not points:
            return

        if layer_image.mode != "RGBA":
            layer_image = layer_image.convert("RGBA")

        brush = BrushUtils.create_soft_brush(self.size, self.color, self.opacity)
        half = self.size // 2

        temp = Image.new("RGBA", layer_image.size, (0, 0, 0, 0))

        all_points = []
        for i in range(len(points) - 1):
            all_points.extend(list(BrushUtils.interpolate(points[i], points[i + 1])))

        all_points.append(points[-1])

        for x, y in all_points:
            temp.paste(brush, (x - half, y - half), brush)

        # Single composite pass to avoid halos
        layer_image.alpha_composite(temp)