from PIL import Image


class Layer:
    """Represents a single image layer."""

    def __init__(self, image=None, name="Layer", width=800, height=600, opacity=100):
        if image is None:
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        image = image.convert("RGBA")
        self.original_image = image.copy()
        self.image = image.copy()
        self.name = name
        self.visible = True
        self.opacity = opacity
        self.filter_id = "normal"
        self.filter_params = {}

    def get_image_with_opacity(self, image=None):
        """Return a copy of the layer image adjusted for opacity."""

        img = image if image else self.image

        if img is None:
            return None

        img = img.convert("RGBA")

        if self.opacity == 100:
            return img.copy()

        r, g, b, a = img.split()
        factor = self.opacity / 100.0
        a = a.point(lambda p: int(p * factor))

        return Image.merge("RGBA", (r, g, b, a))
