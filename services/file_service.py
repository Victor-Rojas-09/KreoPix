from tkinter import filedialog
from PIL import Image
from core.project import Project

class FileService:
    """Handles file I/O operations."""

    def open_image(self):
        """Open an image using a file dialog."""
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
            project = Project(image=image)
            return project, path

        except Exception as e:
            print(f"Error opening file: {e}")
            return None, None

    def open_from_path(self, path):
        """Open an image directly from a known path."""
        try:
            image = Image.open(path).convert("RGBA")
            return Project(image=image)

        except Exception as e:
            print(f"Error opening recent file: {e}")
            return None

    def save_project(self, project):
        """Save the current file."""
        if not project:
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
            final_image = project.composite()
            final_image.save(path)
            return path

        except Exception as e:
            print(f"Error saving file: {e}")
            return None