from PIL import Image
from core.image.image_format import ImageFormat
from core.image.layer import Layer


class ImageService:
    """Handles image operations and creation of ImageFormat documents."""

    # -----------------------------
    # Create blank document
    # -----------------------------
    @staticmethod
    def create_blank_format(width=800, height=600) -> ImageFormat:
        """Create a new blank ImageFormat with a base transparent layer."""
        return ImageFormat(width, height)

    # -----------------------------
    # Open image into ImageFormat
    # -----------------------------
    @staticmethod
    def open_image_format(path) -> ImageFormat:
        """Open an image file and wrap it in an ImageFormat."""
        image = Image.open(path).convert("RGBA")
        width, height = image.size
        doc = ImageFormat(width, height)
        imported_layer = Layer(image, "Imported Image")
        doc.layers.append(imported_layer)
        return doc

    # -----------------------------
    # Layer operations
    # -----------------------------
    @staticmethod
    def set_layer_visibility(layer: Layer, visible: bool):
        """Set the visibility of a layer."""
        layer.visible = visible

    @staticmethod
    def set_layer_opacity(layer: Layer, opacity: int):
        """
        Set the opacity of a layer (0-100) and update its image alpha.
        """
        layer.opacity = opacity
        alpha_factor = opacity / 100.0

        # Aplicar alpha si la capa tiene imagen
        if layer.image:
            img = layer.image.convert("RGBA")
            alpha = img.getchannel('A')
            new_alpha = alpha.point(lambda p: int(p * alpha_factor))

            temp_img = img.copy()
            temp_img.putalpha(new_alpha)
            layer.image = temp_img