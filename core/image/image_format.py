from PIL import Image
from core.image.layer import Layer

class ImageFormat:
    """Editable document with multiple layers."""

    def __init__(self, width=800, height=600, image=None):
        """
        Initialize a new document.
        If an image is provided, create background + image layer.
        Otherwise, create a blank background.
        """
        self.layers = []

        if image:
            self.width, self.height = image.size
            bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
            self.layers.append(Layer(bg, name="Background"))
            self.layers.append(Layer(image, name="Layer 1"))
        else:
            self.width = width
            self.height = height
            # Transparent background for blank project
            bg = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            self.layers.append(Layer(bg, name="Background"))

    def get_size(self):
        """Return project size (width, height)."""
        return self.layers[0].image.size

    def get_layers(self):
        """Return all layers."""
        return list(self.layers)

    def composite(self):
        """Combine all visible layers into one image."""
        base = Image.new("RGBA", self.get_size(), (0, 0, 0, 0))
        for layer in self.layers:
            img = layer.get_image_with_opacity()
            if img:
                base = Image.alpha_composite(base, img)
        return base

    def add_layer(self, name="Layer"):
        new_layer = Layer(
            Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255)),
            name=name
        )
        self.layers.append(new_layer)
        return new_layer
