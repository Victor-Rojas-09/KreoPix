from PIL import Image

class Layer:
    """Represents a single image layer."""

    def __init__(self, image=None, name="Layer", width=800, height=600):
        # Si no se pasa imagen, se crea una imagen transparente del tamaño del proyecto
        if image is None:
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        self.original_image = image.copy()  # copia para restaurar o aplicar opacidad
        self.image = image.copy()
        self.name = name
        self.visible = True
        self.opacity = 100