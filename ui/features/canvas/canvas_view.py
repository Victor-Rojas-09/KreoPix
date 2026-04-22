import tkinter as tk
from ui.widgets.sliders import BlueSlider
from ui.features.canvas.image_renderer import ImageRenderer
from ui.features.canvas.viewport_manager import ViewportManager
from ui.features.canvas.interaction_handler import InteractionHandler, _STROKE_TOOLS


class CanvasView(tk.Frame):
    """Central canvas panel responsible for layout and visual orchestration."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller

        self.current_image = None
        self.tk_image = None
        self._zoom_preview_id = None
        self._transform_overlay_tk = None
        self._bound_state = None

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_top_bar()
        self._build_viewport_area()

        # dependency injection
        self.viewport = ViewportManager(self)
        self.interaction = InteractionHandler(self)

        self.bind("<Configure>", self._on_resize)
        if self.controller:
            self.rebind_state_listener()

    def rebind_state_listener(self):
        """Attach listeners to the active tab's AppState."""

        if not self.controller: return
        if self._bound_state is not None:
            self._bound_state.remove_listener(self.refresh_canvas)
        self._bound_state = self.controller.state
        self._bound_state.add_listener(self.refresh_canvas)

    # =========================================================
    # Construction
    # =========================================================

    def _build_top_bar(self):
        """Create the brush configuration toolbar."""

        self.top_bar = tk.Frame(self, bg="#333")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_remove()

        self.top_inner = tk.Frame(self.top_bar, bg="#333")
        self.top_inner.pack(anchor="center")

        tk.Label(self.top_inner, text="Opacity", bg="#333", fg="white").pack(side="left", padx=8)
        self.brush_opacity_slider = BlueSlider(
            self.top_inner,
            min_value=0,
            max_value=100,
            initial_value=100,
            command=lambda v: self.controller.request_update_brush_opacity(v) if self.controller else None
        )
        self.brush_opacity_slider.pack(side="left", padx=5, pady=10)

        tk.Label(self.top_inner, text="Size", bg="#333", fg="white").pack(side="left", padx=8)
        self.brush_size_slider = BlueSlider(
            self.top_inner,
            min_value=1,
            max_value=400,
            initial_value=70,
            command=lambda v: self.controller.request_update_brush_size(v) if self.controller else None
        )
        self.brush_size_slider.pack(side="left", padx=5, pady=10)

    def _build_viewport_area(self):
        """Build the main canvas widget and the optional scroll sliders."""

        # Top container
        self.viewport_frame = tk.Frame(self, bg="#1e1e1e")
        self.viewport_frame.grid(row=1, column=0, sticky="nsew")
        self.viewport_frame.rowconfigure(0, weight=1)
        self.viewport_frame.columnconfigure(0, weight=1)

        # Inner centered container
        self.canvas = tk.Canvas(self.viewport_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scroll = tk.Scale(
            self.viewport_frame,
            from_=0,
            to=100,
            orient="vertical",
            showvalue=False,
            length=120,
            command=lambda v: self.viewport.handle_scroll(v, "y"),
            bg="#333",
            troughcolor="#2a2a2a",
            highlightthickness=0
        )

        self.h_scroll = tk.Scale(
            self.viewport_frame,
            from_=0,
            to=100,
            orient="horizontal",
            showvalue=False,
            length=120,
            command=lambda v: self.viewport.handle_scroll(v, "x"),
            bg="#333",
            troughcolor="#2a2a2a",
            highlightthickness=0
        )

    # =========================================================
    # Drivers for the Controller
    # =========================================================

    def zoom_to_image_rect(self, x0, y0, x1, y1):
        """Zoom rectangle area."""

        self.viewport.zoom_to_rect(x0, y0, x1, y1)

    def set_viewport_from_session(self, session):
        """Set viewport from session."""

        self.viewport.restore_from_session(session)

    def _update_toolbar_visibility(self):
        """Show or hide the brush settings toolbar based on the active tool."""

        t = self.controller.state.current_tool if self.controller else None

        if t in _STROKE_TOOLS:
            self.top_bar.grid()
        else:
            self.top_bar.grid_remove()

    def display_image(self, pil_image):
        """Entry Point."""

        self.current_image = pil_image
        self._render_image()

    def refresh_canvas(self, state=None):
        """Refresh canvas content. UI never calls services directly."""

        self._update_toolbar_visibility()

        if not self.controller:
            return

        state = self.controller.state
        document = state.get_format()

        if not document:
            return

        if state.has_active_transform():
            # Single entry-point through the controller — no service calls from UI
            composite = self.controller.get_transform_preview()
            if composite is None:
                composite = document.composite()
        else:
            composite = document.composite()

        self.display_image(composite)

    def _on_resize(self, event):
        """Handle resize."""

        if self.current_image:
            self.viewport.sync_transform()
            self._render_image()

    def _render_image(self):
        """Core render function."""

        if self.current_image is None:
            return

        # Clear previous transform overlay
        if self._transform_overlay_tk:
            self.canvas.delete(self._transform_overlay_tk)
            self._transform_overlay_tk = None

        self.canvas.update_idletasks()
        self.viewport.sync_transform()

        # Render image
        tk_image, data = ImageRenderer.render(
            self.canvas,
            self.current_image,
            zoom=self.viewport.transform.zoom,
            offset_x=self.viewport.transform.offset_x,
            offset_y=self.viewport.transform.offset_y,
        )
        if tk_image is None:
            return

        # Update transform again
        self.tk_image = tk_image
        canvas_w, canvas_h, img_w, img_h = data

        self.viewport.transform.update(
            canvas_w, canvas_h, img_w, img_h,
            self.viewport.zoom_factor, self.viewport.offset_x, self.viewport.offset_y
        )

        self.viewport.offset_x = self.viewport.transform.offset_x
        self.viewport.offset_y = self.viewport.transform.offset_y

        # Persist viewport and update
        self.viewport.persist_viewport()
        self.viewport.update_scroll_visibility()
        self._draw_selection_overlay()

    # =========================================================
    # Overlay helpers
    # =========================================================

    def _draw_zoom_preview(self, x0, y0, x1, y1):
        """Temporary Rectangle."""

        # Clear previous preview
        self._clear_zoom_preview()

        # Convert coordinates
        cx0, cy0 = self.viewport.transform.image_to_canvas(x0, y0)
        cx1, cy1 = self.viewport.transform.image_to_canvas(x1, y1)

        # Draw rectangle
        self._zoom_preview_id = self.canvas.create_rectangle(
            cx0,
            cy0,
            cx1,
            cy1,
            outline="#888888",
            dash=(4, 3),
            width=1
        )

    def _clear_zoom_preview(self):
        """Deletes temporary rectangle."""

        if self._zoom_preview_id:
            self.canvas.delete(self._zoom_preview_id)
            self._zoom_preview_id = None

    def _draw_selection_overlay(self):
        """Selection Visualization."""

        if not self.controller:
            return

        document = self.controller.state.get_format()

        if not document:
            return

        # Get selection mask
        mask = self.controller.state.get_selection_mask(document.get_size())
        if mask is None:
            return

        # Get bounding box
        bbox = mask.getbbox()
        if not bbox:
            return

        # Convert to canvas coords
        x0, y0, x1, y1 = bbox
        cx0, cy0 = self.viewport.transform.image_to_canvas(x0, y0)
        cx1, cy1 = self.viewport.transform.image_to_canvas(x1, y1)

        # Draw rectangle
        self.canvas.create_rectangle(
            cx0,
            cy0,
            cx1,
            cy1,
            outline="#555555",
            dash=(5, 3),
            width=1
        )
