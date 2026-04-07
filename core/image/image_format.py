from PIL import Image
from core.image.layer import Layer
from services.filters.filter_service import (
    BlendService,
    FilterService
)

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

    def add_layer(self, name="Layer", insert_at=None):
        """Add a new layer. If insert_at is set, inserts at that index (0 = bottom)."""

        new_layer = Layer(
            Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0)),
            name=name
        )
        if insert_at is None:
            self.layers.append(new_layer)
        else:
            insert_at = max(0, min(int(insert_at), len(self.layers)))
            self.layers.insert(insert_at, new_layer)
        return new_layer

    def composite(self, blend_service=None, filter_service=None):
        """Render final image by compositing all visible layers."""

        if blend_service is None:
            blend_service = BlendService()
        if filter_service is None:
            filter_service = FilterService()

        base_image = None

        for layer in self.layers:
            if not layer.visible:
                continue

            layer_image = layer.image
            if layer_image is None:
                continue

            # Apply filter
            filtered_image = filter_service.apply(
                layer_image,
                layer.filter_id,
                layer.filter_params
            )

            # Apply opacity
            final_layer_image = layer.get_image_with_opacity(filtered_image)

            if final_layer_image is None:
                continue

            # Blend
            if base_image is None:
                base_image = final_layer_image.copy()
            else:
                base_image = blend_service.blend(base_image, final_layer_image)

        return base_image