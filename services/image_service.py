from PIL import Image
from core.project import Project


class ImageService:
    """Handles image operations and project creation."""

    @staticmethod
    def create_blank_project(width=800, height=600):
        return Project(width=width, height=height)

    @staticmethod
    def open_image_project(path):
        image = Image.open(path).convert("RGBA")
        return Project(image=image)

    @staticmethod
    def set_layer_visibility(layer, visible):
        layer.visible = visible

    @staticmethod
    def set_layer_opacity(layer, opacity):
        """Apply the opacity of the given layer and set it visible."""
        layer.opacity = opacity
        alpha_factor = opacity / 100.0

        if hasattr(layer, 'original_image') and layer.original_image:
            img = layer.original_image.convert("RGBA")

            alpha = img.getchannel('A')
            new_alpha = alpha.point(lambda p: int(p * alpha_factor))

            temp_img = img.copy()
            temp_img.putalpha(new_alpha)

            layer.image = temp_img