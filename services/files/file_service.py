from tkinter import filedialog
from services.images.image_service import ImageService
from core.image.image_format import ImageFormat

class FileService:
    """Handles file I/O operations for ImageFormat documents."""

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
            image_format = ImageService.open_image_format(path)
            return image_format, path
        except Exception as e:
            print(f"Error opening file: {e}")
            return None, None

    def open_from_path(self, path):
        """Open an image directly from a known path and wrap in ImageFormat."""
        try:
            return ImageService.open_image_format(path)
        except Exception as e:
            print(f"Error opening recent file: {e}")
            return None

    def save_project(self, image_format: ImageFormat):
        """Save the current ImageFormat to disk as PNG/JPEG."""
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
