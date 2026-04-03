class ColorPickerService:

    def pick_color(self, layer, x: int, y: int):
        """Pick color from layer image."""

        image = layer.image  # NumPy array

        h, w = image.shape[:2]

        if not (0 <= x < w and 0 <= y < h):
            return None

        return tuple(image[y, x])