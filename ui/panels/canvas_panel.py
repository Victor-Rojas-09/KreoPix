import tkinter as tk
from PIL import Image, ImageTk

class CanvasPanel(tk.Frame):
    """Central canvas used to display the composited image."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.current_image = None
        self.tk_image = None

        # Redraw image when panel resizes
        self.bind("<Configure>", self._on_resize)

        # Register listener to AppState
        if self.controller and self.controller.state:
            self.controller.state.add_listener(self.refresh_canvas)

    # --------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------
    def display_image(self, pil_image):
        """Receive a PIL image and display it."""
        self.current_image = pil_image
        self._draw_scaled()

    def refresh_canvas(self, state):
        """Refresh canvas when state changes."""
        document = state.get_format()
        if document:
            image = document.composite()
            self.display_image(image)

    # --------------------------------------------------
    # INTERNAL LOGIC
    # --------------------------------------------------
    def _on_resize(self, event):
        """Redraw image on resize."""
        if self.current_image:
            self._draw_scaled()

    def _draw_scaled(self):
        """Scale image to fit the canvas while preserving aspect ratio."""
        if self.current_image is None:
            return

        self.update_idletasks()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w < 10:
            return

        img_w, img_h = self.current_image.size
        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = self.current_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.canvas.create_image(canvas_w // 2, canvas_h // 2, image=self.tk_image, anchor="center")
