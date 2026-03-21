from PIL import Image

class Layer:
    """Represents a single image layer."""

    def __init__(self, image=None, name="Layer", width=800, height=600):
        if image is None:
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        self.original_image = image.copy()
        self.image = image.copy()
        self.name = name
        self.visible = True
        self.opacity = 100
        self.mode = "Normal"

    def get_image_with_opacity(self):
        """Return the image with applied opacity if visible."""

        if not self.visible:
            return None

        img = self.image.copy()

        if self.opacity < 100:
            alpha = img.getchannel("A")
            alpha = alpha.point(lambda p: int(p * (self.opacity / 100)))
            img.putalpha(alpha)
        return img
