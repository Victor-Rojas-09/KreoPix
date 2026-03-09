from PIL import Image

class Layer:
    """Represents a single image layer."""

    def __init__(self, image, name="Layer"):
        self.original_image = image
        self.image = image.copy()

        self.name = name
        self.visible = True
        self.opacity = 100

class Project:
    """Represents an editing project with layers."""

    def __init__(self, width=800, height=600, image=None):
        self.layers = []

        if image:
            self.width, self.height = image.size

            # Background layer
            bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
            self.layers.append(Layer(bg, name="Background"))

            # Image layer
            self.layers.append(Layer(image, name="Layer 1"))
        else:
            self.width = width
            self.height = height
            bg = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            self.layers.append(Layer(bg, name="Background"))


    def get_size(self):
        """Get the size of the project."""
        return self.layers[0].image.size

    def get_layers(self):
        """Return the layers."""
        return self.layers

    def composite(self):
        """Composite all visible layers."""
        base = Image.new("RGBA", self.get_size(), (0, 0, 0, 0))

        for layer in self.layers:
            if layer.visible:
                base = Image.alpha_composite(base, layer.image)

        return base

    def add_layer(self, layer):
        self.layers.append(layer)
