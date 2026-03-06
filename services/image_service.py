from PIL import Image
from core.project import Project, Layer

class ImageService:
    """Handles image operations and project creation."""

    def create_blank_project(self, width=800, height=600):
        """Make a blank layer with given width and height."""
        return Project(width=width, height=height)

    def open_image_project(self, path):
        """Open an image file at given path anc return in RGBA format."""
        image = Image.open(path).convert("RGBA")

        return Project(image=image)

    def set_layer_visibility(self, layer, visible):
        layer.visible = visible

    def set_layer_opacity(self, layer, opacity):
        """Applay the opacity of the given layer and set it visible."""
        layer.opacity = opacity
        alpha_factor = opacity / 100.0

        if hasattr(layer, 'original_image') and layer.original_image:
            img = layer.original_image.convert("RGBA")
            r, g, b, a = img.split()

            # Multiply the alpha channel by the opacity factor.
            new_alpha = a.point(lambda p: int(p * alpha_factor))
            layer.image = Image.merge("RGBA", (r, g, b, new_alpha))