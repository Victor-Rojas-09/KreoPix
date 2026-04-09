from PIL import Image, ImageTk


class ImageRenderer:
    """Draw the full document image with viewport transform only."""

    @staticmethod
    def render(canvas, pil_image, zoom: float, offset_x: float, offset_y: float):
        """Render the full image scaled by zoom, placed at (offset_x, offset_y), anchor nw."""

        canvas.update_idletasks()

        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        img_w, img_h = pil_image.size

        meta = (canvas_w, canvas_h, img_w, img_h)

        if canvas_w < 1 or canvas_h < 1:
            return None, meta

        if zoom <= 0:
            zoom = 1e-6

        disp_w = max(1, int(round(img_w * zoom)))
        disp_h = max(1, int(round(img_h * zoom)))

        display_rgb = pil_image.convert("RGBA").resize((disp_w, disp_h), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(display_rgb)

        canvas.delete("all")
        canvas.create_image(
            int(round(offset_x)),
            int(round(offset_y)),
            anchor="nw",
            image=tk_image,
        )

        return tk_image, meta
