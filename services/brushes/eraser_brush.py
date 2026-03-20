from PIL import Image
from services.brushes.base_brush import BaseBrush
from services.brushes.utils.brush_utils import BrushUtils


class EraserBrush(BaseBrush):
    """
    Eraser brush that removes opacity from the layer.

    Instead of painting color, this brush reduces the alpha channel,
    effectively erasing pixels.

    Characteristics:
    - Works on alpha channel
    - Supports soft or hard edges
    - Non-destructive to color data (only affects transparency)
    """

    def apply_stroke(self, layer_image, points):
        if not points:
            return

        if layer_image.mode != "RGBA":
            layer_image = layer_image.convert("RGBA")

        # Soft eraser (puedes cambiar a hard si quieres)
        brush = BrushUtils.create_soft_brush(self.size, (0, 0, 0, 255), self.opacity)
        half = self.size // 2

        temp = Image.new("RGBA", layer_image.size, (0, 0, 0, 0))

        all_points = []
        for i in range(len(points) - 1):
            all_points.extend(list(BrushUtils.interpolate(points[i], points[i + 1])))
        all_points.append(points[-1])

        for x, y in all_points:
            temp.paste(brush, (x - half, y - half), brush)

        # Convert temp to alpha mask
        r, g, b, a = temp.split()

        # Reduce alpha from original image
        layer_r, layer_g, layer_b, layer_a = layer_image.split()
        new_alpha = ImageChops.subtract(layer_a, a)

        layer_image.putalpha(new_alpha)