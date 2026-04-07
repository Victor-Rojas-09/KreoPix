class ColorPickerService:

    def pick_color(self, layer, x: int, y: int):
        """Pick color from layer image (PIL RGBA)."""

        image = layer.image

        if image is None:
            return None

        w, h = image.size
        if not (0 <= x < w and 0 <= y < h):
            return None

        px = image.getpixel((x, y))
        if not isinstance(px, tuple):
            px = tuple(px)
        if len(px) == 3:
            return px + (255,)
        if len(px) >= 4:
            return tuple(px[:4])
        return None
