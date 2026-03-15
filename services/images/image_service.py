from PIL import Image
from core.image.image_format import ImageFormat
from core.image.layer import Layer

class ImageService:
    """Handles image operations and layer management."""

    @staticmethod
    def create_blank_format(width=800, height=600) -> ImageFormat:
        """Create a new blank ImageFormat with transparent background."""
        return ImageFormat(width, height)

    @staticmethod
    def open_image_format(path) -> ImageFormat:
        """Open an image file and wrap it in an ImageFormat."""
        image = Image.open(path).convert("RGBA")
        return ImageFormat(image=image)

    @staticmethod
    def set_layer_visibility(layer: Layer, visible: bool):
        """Set the visibility of a layer."""
        layer.visible = visible

    @staticmethod
    def set_layer_opacity(layer: Layer, opacity: int):
        """Set the opacity of a layer (0-100)."""
        layer.opacity = max(0, min(opacity, 100))
