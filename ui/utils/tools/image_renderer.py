from PIL import Image, ImageTk


class ImageRenderer:
    """
    Responsible for rendering a PIL image into a Tkinter Canvas.

    This includes:
    - Scaling the image while maintaining aspect ratio
    - Centering the image inside the canvas
    - Converting PIL images into Tkinter-compatible images
    """

    @staticmethod
    def render(canvas, pil_image):
        """Render a PIL image into the given canvas."""
        canvas.update_idletasks()

        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        img_w, img_h = pil_image.size

        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized)

        canvas.delete("all")
        canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=tk_image,
            anchor="center"
        )

        return tk_image, (canvas_w, canvas_h, img_w, img_h)