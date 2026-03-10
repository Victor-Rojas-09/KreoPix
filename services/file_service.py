from tkinter import filedialog
from PIL import Image
from core.image.image_format import ImageFormat
from core.image.layer import Layer


class FileService:
    """Handles file I/O operations using the new ImageFormat."""

    # -------------------------
    # Open image via dialog
    # -------------------------
    def open_image(self):
        """Open an image using a file dialog and wrap it in ImageFormat."""
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Bitmap", "*.bmp"),
                ("All Files", "*.*"),
            ]
        )

        if not path:
            return None, None

        try:
            image = Image.open(path).convert("RGBA")
            image_format = self._create_image_format_from_image(image)
            return image_format, path

        except Exception as e:
            print(f"Error opening file: {e}")
            return None, None

    # -------------------------
    # Open image from path
    # -------------------------
    def open_from_path(self, path):
        """Open an image directly from a known path and wrap in ImageFormat."""
        try:
            image = Image.open(path).convert("RGBA")
            return self._create_image_format_from_image(image)

        except Exception as e:
            print(f"Error opening recent file: {e}")
            return None

    # -------------------------
    # Save current ImageFormat
    # -------------------------
    def save_project(self, image_format):
        """Save the current ImageFormat to disk."""
        if not image_format:
            return None

        path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("All Files", "*.*"),
            ]
        )

        if not path:
            return None

        try:
            final_image = image_format.composite()
            final_image.save(path)
            return path

        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    # -------------------------
    # Helpers
    # -------------------------
    @staticmethod
    def _create_image_format_from_image(image: Image.Image) -> ImageFormat:
        """Wrap a PIL image in an ImageFormat with background layer."""
        width, height = image.size
        doc = ImageFormat(width, height)

        # Replace default background with actual image
        imported_layer = Layer(image, "Imported Image")

        # Mantener fondo transparente + imagen importada
        doc.layers.append(imported_layer)

        return doc