import tkinter as tk
from ui.utils.tools.custom_slider import BlueSlider
from ui.utils.tools.canvas_transform import CanvasTransform
from ui.utils.tools.image_renderer import ImageRenderer


class CanvasPanel(tk.Frame):
    """Central canvas panel responsible for rendering and interacting with the image."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller

        # Transformation helper
        self.transform = CanvasTransform()

        # Image state
        self.current_image = None
        self.tk_image = None
        self._stroke_points = []

        # Layout
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_top_bar()
        self._build_canvas()

        # Events
        self.bind("<Configure>", self._on_resize)

        if self.controller and self.controller.state:
            self.controller.state.add_listener(self.refresh_canvas)

    # =========================================================
    # UI Construction
    # =========================================================

    def _build_top_bar(self):
        """Create brush configuration toolbar."""
        self.top_bar = tk.Frame(self, bg="#333")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_remove()

        self.top_inner = tk.Frame(self.top_bar, bg="#333")
        self.top_inner.pack(anchor="center")

        tk.Label(self.top_inner, text="Opacity", bg="#333", fg="white").pack(side="left", padx=5)
        self.opacity_slider = BlueSlider(self.top_inner, command=self._on_opacity_change)
        self.opacity_slider.pack(side="left", padx=5)

        tk.Label(self.top_inner, text="Size", bg="#333", fg="white").pack(side="left", padx=5)
        self.size_slider = BlueSlider(self.top_inner, command=self._on_size_change)
        self.size_slider.pack(side="left", padx=5)

    def _build_canvas(self):
        """Create drawing canvas and bind mouse events."""
        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

    # =========================================================
    # Brush Configuration
    # =========================================================

    def _on_opacity_change(self, value):
        """Handle brush opacity changes from the UI."""

        if self.controller:
            self.controller.request_update_brush_opacity(value)

    def _on_size_change(self, value):
        """Handle brush size changes from the UI."""

        if self.controller:
            self.controller.request_update_brush_size(value)

    # =========================================================
    # Mouse Interaction
    # =========================================================

    def _on_mouse_down(self, event):
        """Start a new brush stroke."""

        if not self._brush_active():
            return

        self._stroke_points = [
            self.transform.canvas_to_image(event.x, event.y)
        ]

    def _on_mouse_move(self, event):
        """Continue recording a brush stroke while the mouse moves."""

        if not self._brush_active():
            return

        self._stroke_points.append(
            self.transform.canvas_to_image(event.x, event.y)
        )

    def _on_mouse_up(self, event):
        """Finalize and apply the brush stroke."""
        if not self._brush_active():
            return

        self._stroke_points.append(
            self.transform.canvas_to_image(event.x, event.y)
        )

        if self.controller:
            self.controller.handle_paint_stroke(self._stroke_points)

        self._stroke_points = []

    def _brush_active(self):
        """Check if brush tool is active."""

        return self.controller and self.controller.state.current_tool == "brush"

    def _update_toolbar_visibility(self):
        """Show or hide brush toolbar based on active tool."""

        if self._brush_active():
            self.top_bar.grid()
        else:
            self.top_bar.grid_remove()

    # =========================================================
    # Rendering
    # =========================================================

    def display_image(self, pil_image):
        """Set and render a new image."""

        self.current_image = pil_image
        self._render_image()

    def refresh_canvas(self, state=None):
        """Refresh canvas from controller state."""

        self._update_toolbar_visibility()

        document = self.controller.state.get_format()
        if document:
            image = document.composite()
            self.display_image(image)

    def _on_resize(self, event):
        """Handle resize and re-render image."""

        if self.current_image:
            self._render_image()

    def _render_image(self):
        """Render image and update transform."""

        if self.current_image is None:
            return

        self.tk_image, data = ImageRenderer.render(self.canvas, self.current_image)

        canvas_w, canvas_h, img_w, img_h = data
        self.transform.update(canvas_w, canvas_h, img_w, img_h)