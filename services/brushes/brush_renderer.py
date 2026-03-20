from PIL import Image, ImageChops


class BrushRenderer:
    """Handles how brush stamps are applied to the image."""

    def __init__(self, mode="normal"):
        self.mode = mode
        self._temp = None

    def begin(self, layer):
        """Called at the start of a stroke."""

        if self.mode == "accumulate":
            self._temp = Image.new("RGBA", layer.size, (0, 0, 0, 0))

    def apply(self, layer, stamp, x, y):
        """Apply a single stamp."""

        half = stamp.size[0] // 2

        if self.mode == "normal":
            layer.paste(stamp, (x - half, y - half), stamp)

        elif self.mode == "accumulate":
            self._temp.paste(stamp, (x - half, y - half), stamp)

        elif self.mode == "erase":
            mask = stamp.split()[-1]

            temp = Image.new("L", layer.size, 0)
            temp.paste(mask, (x - half, y - half))

            r, g, b, a = layer.split()
            new_alpha = ImageChops.subtract(a, temp)
            layer.putalpha(new_alpha)

    def end(self, layer):
        """Called at the end of a stroke."""

        if self.mode == "accumulate" and self._temp:
            layer.alpha_composite(self._temp)