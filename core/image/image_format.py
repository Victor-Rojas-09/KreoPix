from PIL import Image
from core.image.layer import Layer


class ImageFormat:
    """
    Internal image format used by the editor.

    Stores:
    - canvas size
    - layers
    """

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.layers = []

        # create base transparent layer
        base = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.layers.append(Layer(base, "Background"))

    # --------------------------------------------------
    # Layer management
    # --------------------------------------------------

    def add_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        if layer in self.layers:
            self.layers.remove(layer)

    def get_layers(self):
        return self.layers

    # --------------------------------------------------
    # Canvas composite
    # --------------------------------------------------

    def composite(self):
        """
        Merge all visible layers into a single image.
        """

        base = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))

        for layer in self.layers:

            if not layer.visible:
                continue

            base.alpha_composite(
                layer.image,
                (layer.x, layer.y)
            )

        return base