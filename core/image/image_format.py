from PIL import Image
from core.image.layer import Layer

class ImageFormat:
    """Represents an editable document with multiple layers."""

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.layers = []

        # Capa base inicial
        self.layers.append(Layer(width=width, height=height, name="Background"))

    def get_size(self):
        return (self.width, self.height)

    def get_layers(self):
        return list(self.layers)

    def composite(self):
        """Combine all visible layers into one image."""
        base = Image.new("RGBA", self.get_size(), (0, 0, 0, 0))
        for layer in self.layers:
            if layer.visible and layer.image:
                base = Image.alpha_composite(base, layer.image)
        return base

    def add_layer(self, name="Layer"):
        """Add a new blank layer."""
        new_layer = Layer(width=self.width, height=self.height, name=name)
        self.layers.append(new_layer)
        return new_layer