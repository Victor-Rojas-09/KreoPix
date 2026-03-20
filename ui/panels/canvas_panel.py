import tkinter as tk
from PIL import Image, ImageTk
from ui.utils.tools.custom_slider import BlueSlider


class CanvasPanel(tk.Frame):
    """
    Central canvas panel responsible for rendering and interacting with the image.
    This component acts as the visual layer of the painting system.
    """

    def __init__(self, parent, controller=None):
        """
        Initialize the CanvasPanel.

        Args:
            parent: Parent Tkinter widget
            controller: Controller handling application logic
        """
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller

        # -------------------------
        # Layout (GRID)
        # -------------------------
        self.rowconfigure(0, weight=0)  # Top toolbar
        self.rowconfigure(1, weight=1)  # Canvas area
        self.columnconfigure(0, weight=1)

        # -------------------------
        # Top Bar (Brush Settings)
        # -------------------------
        self.top_bar = tk.Frame(self, bg="#333")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_remove()  # Hidden by default

        self.top_inner = tk.Frame(self.top_bar, bg="#333")
        self.top_inner.pack(anchor="center")

        tk.Label(self.top_inner, text="Opacity", bg="#333", fg="white").pack(side="left", padx=5)
        self.opacity_slider = BlueSlider(self.top_inner, command=self._on_opacity_change)
        self.opacity_slider.pack(side="left", padx=5)

        tk.Label(self.top_inner, text="Size", bg="#333", fg="white").pack(side="left", padx=5)
        self.size_slider = BlueSlider(self.top_inner, command=self._on_size_change)
        self.size_slider.pack(side="left", padx=5)

        # -------------------------
        # Canvas
        # -------------------------
        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.current_image = None
        self.tk_image = None
        self._stroke_points = []

        # Resize handling
        self.bind("<Configure>", self._on_resize)

        # Subscribe to state updates
        if self.controller and self.controller.state:
            self.controller.state.add_listener(self.refresh_canvas)

        # Mouse events for painting
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

    # =========================================================
    # Brush Configuration
    # =========================================================

    def _on_opacity_change(self, value):
        """
        Handle opacity slider updates.

        Args:
            value (int): New opacity value (0–100)
        """
        if self.controller:
            self.controller.request_update_brush_opacity(value)

    def _on_size_change(self, value):
        """
        Handle size slider updates.

        Args:
            value (int): New brush size
        """
        if self.controller:
            self.controller.request_update_brush_size(value)

    def _edit_opacity_value(self, event):
        """Allow manual editing of opacity value via text input."""
        self._edit_slider_value(self.opacity_slider, self.controller.request_update_brush_opacity)

    def _edit_size_value(self, event):
        """Allow manual editing of size value via text input."""
        self._edit_slider_value(self.size_slider, self.controller.request_update_brush_size)

    def _edit_slider_value(self, slider, callback):
        """
        Replace a slider temporarily with an input field for manual value entry.

        Args:
            slider: Slider instance to edit
            callback: Function to call when value changes
        """
        entry = tk.Entry(self.top_bar, width=5)
        entry.insert(0, str(slider.get_value()))
        entry.pack(side="left", padx=5)

        def apply_value(event=None):
            try:
                val = int(entry.get())
                slider.set_value(val)
                callback(val)
            except ValueError:
                pass
            entry.destroy()

        entry.bind("<Return>", apply_value)
        entry.bind("<FocusOut>", apply_value)
        entry.focus_set()

    # =========================================================
    # Mouse Interaction (Painting)
    # =========================================================

    def _on_mouse_down(self, event):
        """Start a new brush stroke."""
        if not self._brush_active():
            return
        self._stroke_points = [self._canvas_to_image_coords(event.x, event.y)]

    def _on_mouse_move(self, event):
        """Add points to the current stroke while dragging."""
        if not self._brush_active():
            return
        self._stroke_points.append(self._canvas_to_image_coords(event.x, event.y))

    def _on_mouse_up(self, event):
        """
        Finalize the stroke and send it to the controller.

        The full list of collected points is passed as a single stroke.
        """
        if not self._brush_active():
            return

        self._stroke_points.append(self._canvas_to_image_coords(event.x, event.y))

        if self.controller:
            self.controller.handle_paint_stroke(self._stroke_points)

        self._stroke_points = []

    def _brush_active(self):
        """
        Check if the brush tool is currently active.

        Also toggles visibility of the brush configuration UI.

        Returns:
            bool: True if brush tool is active, False otherwise
        """
        if self.controller and self.controller.state.current_tool == "brush":
            self.top_bar.grid()
            return True
        else:
            self.top_bar.grid_remove()
            return False

    # =========================================================
    # Rendering
    # =========================================================

    def display_image(self, pil_image):
        """
        Set and render a new image.

        Args:
            pil_image (PIL.Image): Image to display
        """
        self.current_image = pil_image
        self._draw_scaled()

    def refresh_canvas(self, state=None):
        """
        Refresh the canvas from the current document state.

        This method is typically triggered by state listeners.
        """
        document = self.controller.state.get_format()
        if document:
            image = document.composite()
            self.display_image(image)

    def _on_resize(self, event):
        """Handle panel resizing and redraw the image."""
        if self.current_image:
            self._draw_scaled()

    def _draw_scaled(self):
        """
        Scale and center the current image within the canvas.

        Maintains aspect ratio and uses high-quality resampling.
        """
        if self.current_image is None:
            return

        self.update_idletasks()

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.current_image.size

        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        resized = self.current_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=self.tk_image,
            anchor="center"
        )

    # =========================================================
    # Coordinate Mapping
    # =========================================================

    def _canvas_to_image_coords(self, cx, cy):
        """
        Convert canvas coordinates to image coordinates.

        This accounts for:
        - Image scaling
        - Centering offsets
        - Boundary clamping

        Args:
            cx (int): Canvas X coordinate
            cy (int): Canvas Y coordinate

        Returns:
            tuple: (x, y) coordinates in image space
        """
        if not self.current_image:
            return (0, 0)

        img_w, img_h = self.current_image.size
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        offset_x = (canvas_w - new_w) // 2
        offset_y = (canvas_h - new_h) // 2

        ix = int((cx - offset_x) / scale)
        iy = int((cy - offset_y) / scale)

        return (
            max(0, min(img_w - 1, ix)),
            max(0, min(img_h - 1, iy))
        )