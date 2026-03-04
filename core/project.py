from PIL import Image


class Layer:
    """Represents a single layer."""

    def __init__(self, image, name):
        self.image = image
        self.name = name
        self.visible = True


class Project:
    """Represents an editing project with layers."""

    def __init__(self, width=None, height=None, image=None):
        self.layers = []

        if image:
            # Open a project
            base = Image.new("RGBA", image.size, "white")
            self.layers.append(Layer(base, "Layer 0"))

            self.layers.append(Layer(image, "Layer 1"))

        else:
            # Create a new project
            base = Image.new("RGBA", (width, height), "white")
            self.layers.append(Layer(base, "Layer 0"))


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