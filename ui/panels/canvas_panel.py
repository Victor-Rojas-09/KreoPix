import tkinter as tk
from core.library.transform.scaling import compute_region_zoom_factor
from ui.utils.tools.custom_slider import BlueSlider
from ui.utils.tools.canvas_transform import CanvasTransform
from ui.utils.tools.image_renderer import ImageRenderer

_STROKE_TOOLS = frozenset({"brush", "eraser"})

class CanvasPanel(tk.Frame):
    """Central canvas panel responsible for rendering and interacting with the image."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller

        self.transform = CanvasTransform()

        self.current_image = None
        self.tk_image = None
        self._stroke_points = []
        self._zoom_rect_start = None
        self._zoom_preview_id = None

        self.zoom_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self._suppress_scroll = False

        # Layout Configuration
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_top_bar()
        self._build_viewport_area()

        # Resize Binding
        self.bind("<Configure>", self._on_resize)

        # State Binding System
        self._bound_state = None
        if self.controller:
            self.rebind_state_listener()

        self._bind_zoom_shortcuts()

    # =========================================================
    # State binding (multi-tab)
    # =========================================================

    def rebind_state_listener(self):
        """Attach listeners to the active tab's AppState."""

        if not self.controller:
            return

        # Remove old listener
        if self._bound_state is not None:
            self._bound_state.remove_listener(self.refresh_canvas)

        # Bind new state
        self._bound_state = self.controller.state
        self._bound_state.add_listener(self.refresh_canvas)

    # =========================================================
    # Construction
    # =========================================================

    def _build_top_bar(self):
        """Create brush configuration toolbar."""
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
            command=self._on_opacity_change,
        )

        self.brush_opacity_slider.pack(side="left", padx=5, pady=10)

        tk.Label(self.top_inner, text="Size", bg="#333", fg="white").pack(side="left", padx=8)

        self.brush_size_slider = BlueSlider(
            self.top_inner,
            min_value=1,
            max_value=400,
            initial_value=70,
            command=self._on_size_change,
        )
        self.brush_size_slider.pack(side="left", padx=5, pady=10)

    def _build_viewport_area(self):
        """Canvas with optional scroll sliders."""

        # Top container
        self.viewport = tk.Frame(self, bg="#1e1e1e")
        self.viewport.grid(row=1, column=0, sticky="nsew")
        self.viewport.rowconfigure(0, weight=1)
        self.viewport.columnconfigure(0, weight=1)

        # Inner centered container
        self.canvas = tk.Canvas(self.viewport, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.v_scroll = tk.Scale(
            self.viewport,
            from_=0,
            to=100,
            orient="vertical",
            showvalue=0,
            length=120,
            command=self._on_v_scroll,
            bg="#333",
            troughcolor="#2a2a2a",
            highlightthickness=0,
        )
        self.h_scroll = tk.Scale(
            self.viewport,
            from_=0,
            to=100,
            orient="horizontal",
            showvalue=0,
            length=120,
            command=self._on_h_scroll,
            bg="#333",
            troughcolor="#2a2a2a",
            highlightthickness=0,
        )

        # Mouse event bindings
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

    def _bind_zoom_shortcuts(self):
        """Shortcuts for centered zoom."""

        self.canvas.bind_all("<Control-plus>", self._on_ctrl_zoom_in)
        self.canvas.bind_all("<Control-KP_Add>", self._on_ctrl_zoom_in)
        self.canvas.bind_all("<Control-equal>", self._on_ctrl_zoom_in)
        self.canvas.bind_all("<Control-minus>", self._on_ctrl_zoom_out)
        self.canvas.bind_all("<Control-KP_Subtract>", self._on_ctrl_zoom_out)

    def _on_ctrl_zoom_in(self, event=None):
        """Control zoom in."""

        if not self.controller or not self._is_editor_active():
            return

        self._zoom_at_canvas_center(1.15)

        return "break"

    def _on_ctrl_zoom_out(self, event=None):
        """Control zoom out."""

        if not self.controller or not self._is_editor_active():
            return

        self._zoom_at_canvas_center(1.0 / 1.15)

        return "break"

    def _is_editor_active(self):
        """Return True if editor is active."""

        return self.controller and self.controller.state.has_format()

    def _sync_transform(self):
        """Apply zoom_factor + offsets and clamp."""

        if self.current_image is None:
            return

        self.canvas.update_idletasks()

        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.current_image.size

        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)
        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

    def _zoom_at_canvas_center(self, factor_mult: float):
        """Zoom in and out keeping the canvas center on the same image pixel."""

        if self.current_image is None:
            return
        self.canvas.update_idletasks()

        # Canvas dimensions
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        cx = cw / 2.0
        cy = ch / 2.0

        iw, ih = self.current_image.size

        # Transform synchronization
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)
        z_old = self.transform.zoom

        # Center brush
        ix = (cx - self.transform.offset_x) / z_old if z_old else 0.0
        iy = (cy - self.transform.offset_y) / z_old if z_old else 0.0

        # Apply and recalculate zoom
        self.zoom_factor = max(0.05, min(20.0, self.zoom_factor * factor_mult))
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)
        z_new = self.transform.zoom

        # Transform offsets and repositions
        self.offset_x = cx - ix * z_new
        self.offset_y = cy - iy * z_new
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)
        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

        # Persist and render
        self._persist_viewport()
        self._render_image()

    def set_viewport_from_session(self, session):
        """Restore viewport from an EditorSession."""

        self.zoom_factor = getattr(session, "zoom_factor", 1.0)
        self.offset_x = getattr(session, "offset_x", 0.0)
        self.offset_y = getattr(session, "offset_y", 0.0)

        if self.current_image:
            self._render_image()

    def _persist_viewport(self):
        """Persist viewport to a image."""

        if self.controller:
            self.controller.update_active_session_viewport(
                self.zoom_factor, self.offset_x, self.offset_y
            )

    def zoom_to_image_rect(self, x0, y0, x1, y1):
        """Fit the given image rectangle in the viewport."""

        if self.current_image is None or not self.controller:
            return

        self.canvas.update_idletasks()

        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.current_image.size

        # Compute best zoom
        zf = compute_region_zoom_factor(cw, ch, iw, ih, x0, y0, x1, y1)

        # Clamp zoom
        self.zoom_factor = max(0.05, min(20.0, zf))
        rx0, rx1 = sorted((x0, x1))
        ry0, ry1 = sorted((y0, y1))

        # Find rectangle center
        icx = (rx0 + rx1) / 2.0
        icy = (ry0 + ry1) / 2.0
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, 0.0, 0.0)
        z = self.transform.zoom

        # Center it on canvas
        self.offset_x = cw / 2.0 - icx * z
        self.offset_y = ch / 2.0 - icy * z

        # Clamp again via transform
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)

        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

        # Save and render
        self._persist_viewport()
        self._render_image()

    # =========================================================
    # Brush Configuration
    # =========================================================

    def _on_opacity_change(self, value):
        """Change opacity."""

        if self.controller:
            self.controller.request_update_brush_opacity(value)

    def _on_size_change(self, value):
        """Change size."""

        if self.controller:
            self.controller.request_update_brush_size(value)

    # =========================================================
    # Scroll sliders (refactored)
    # =========================================================

    def _handle_scroll(self, value: float, axis: str):
        """Generic handler for scroll slider movement."""

        if self._suppress_scroll or self.current_image is None:
            return

        # Sync transform state
        self._sync_transform()

        # Select axis-specific logic
        if axis == "x":
            min_o, max_o = self.transform.scroll_range_x()
        elif axis == "y":
            min_o, max_o = self.transform.scroll_range_y()
        else:
            raise ValueError(f"Invalid axis '{axis}', expected 'x' or 'y'.")

        # If no scrolling is needed, exit early
        if abs(max_o - min_o) < 1e-6:
            return

        # Normalize slider value to [0, 1]
        frac = float(value) / 100.0

        # Linear interpolation (inverted mapping)
        offset = (1.0 - frac) * max_o + frac * min_o

        # Assign offset to the correct axis
        if axis == "x":
            self.offset_x = offset
        else:
            self.offset_y = offset

        # Update transform (may clamp values internally)
        self.transform.update(
            self.transform.canvas_w,
            self.transform.canvas_h,
            self.transform.img_w,
            self.transform.img_h,
            self.zoom_factor,
            self.offset_x,
            self.offset_y
        )

        # Read back clamped values
        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

        # Persist and redraw
        self._persist_viewport()
        self._render_image()

    def _update_single_scroll_visibility(self, axis: str):
        """Update visibility and position of a single scroll slider."""

        visibility_threshold = 0.5
        epsilon = 1e-6

        if axis == "x":

            min_o, max_o = self.transform.scroll_range_x()
            scroll_widget = self.h_scroll
            offset = self.offset_x
            grid_kwargs = dict(row=1, column=0, sticky="ew")

        elif axis == "y":

            min_o, max_o = self.transform.scroll_range_y()
            scroll_widget = self.v_scroll
            offset = self.offset_y
            grid_kwargs = dict(row=0, column=1, sticky="ns")

        else:
            raise ValueError(f"Invalid axis '{axis}', expected 'x' or 'y'.")

        # Determine if scrolling is needed
        if abs(max_o - min_o) > visibility_threshold:

            scroll_widget.grid(**grid_kwargs)

            # Convert offset to slider position
            denom = min_o - max_o

            if abs(denom) > epsilon:
                #Prevent recursion
                self._suppress_scroll = True

                try:
                    value = 100.0 * (offset - max_o) / denom
                    scroll_widget.set(value)
                finally:
                    self._suppress_scroll = False
        else:
            #Hide if not needed
            scroll_widget.grid_remove()

    def _on_h_scroll(self, value):
        """Horizontal scroll callback."""

        self._handle_scroll(value, axis="x")

    def _on_v_scroll(self, value):
        """Vertical scroll callback."""

        self._handle_scroll(value, axis="y")

    def _update_scroll_visibility(self):
        """Update visibility of both horizontal and vertical scroll sliders."""

        if self.current_image is None:
            self.v_scroll.grid_remove()
            self.h_scroll.grid_remove()
            return

        self._update_single_scroll_visibility(axis="x")
        self._update_single_scroll_visibility(axis="y")

    # =========================================================
    # Mouse Interaction
    # =========================================================

    def _on_mouse_down(self, event):
        """Handle mouse events, start of action."""

        if not self.controller:
            return

        # Gives position on screen
        self._sync_transform()
        x, y = self.transform.canvas_to_image(event.x, event.y)

        tool = self.controller.state.current_tool

        # Tool-based behavior
        if tool in _STROKE_TOOLS:
            self._stroke_points = [(x, y)]

        elif tool == "eyedropper":
            self.controller.handle_eyedropper(x, y)

        elif tool == "paint_bucket":
            self.controller.handle_fill(x, y)

        elif tool == "select":
            self._selection_start = (x, y)
            self.controller.handle_rect_selection(x, y, x, y)

        elif tool == "magic_wand":
            self.controller.handle_magic_wand(x, y)

        elif tool == "zoom_area":
            self._zoom_rect_start = (x, y)
            self._draw_zoom_preview(x, y, x, y)

    def _on_mouse_move(self, event):
        """Handle mouse move, while dragging."""

        if not self.controller:
            return

        self._sync_transform()
        tool = self.controller.state.current_tool

        # Only zoom area reacts
        if tool not in _STROKE_TOOLS:
            if tool == "zoom_area" and self._zoom_rect_start:

                x0, y0 = self._zoom_rect_start
                x1, y1 = self.transform.canvas_to_image(event.x, event.y)

                self._draw_zoom_preview(x0, y0, x1, y1)
            return

        self._stroke_points.append(self.transform.canvas_to_image(event.x, event.y))

    def _on_mouse_up(self, event):
        """Handle mouse up, the end of action."""

        if not self.controller:
            return

        self._sync_transform()
        tool = self.controller.state.current_tool

        # Selection the area
        if tool not in _STROKE_TOOLS:

            if tool == "select" and self._selection_start:
                x0, y0 = self._selection_start
                x1, y1 = self.transform.canvas_to_image(event.x, event.y)

                self.controller.handle_rect_selection(x0, y0, x1, y1)
                self._selection_start = None

            if tool == "zoom_area" and self._zoom_rect_start:
                x0, y0 = self._zoom_rect_start
                x1, y1 = self.transform.canvas_to_image(event.x, event.y)

                self.controller.handle_zoom_to_rect(x0, y0, x1, y1)
                self._zoom_rect_start = None
                self._clear_zoom_preview()

            return

        # Stroke tools and send full stroke
        self._stroke_points.append(self.transform.canvas_to_image(event.x, event.y))
        self.controller.handle_paint_stroke(self._stroke_points)

        # Reset buffer
        self._stroke_points = []

    def _brush_active(self):
        """Activate brush."""

        t = self.controller.state.current_tool if self.controller else None

        return t in _STROKE_TOOLS

    def _update_toolbar_visibility(self):
        """Show and hide brush settings UI."""

        if self._brush_active():
            self.top_bar.grid()
        else:
            self.top_bar.grid_remove()

    # =========================================================
    # Rendering
    # =========================================================

    def display_image(self, pil_image):
        """Entry Point."""

        self.current_image = pil_image
        self._render_image()

    def refresh_canvas(self, state=None):
        """Refresh canvas."""

        self._update_toolbar_visibility()

        # Get current document
        document = self.controller.state.get_format()

        # Display it
        if document:
            image = document.composite()
            self.display_image(image)

    def _on_resize(self, event):
        """Handle resize."""

        if self.current_image:
            self._sync_transform()
            self._render_image()

    def _render_image(self):
        """Core render function."""

        if self.current_image is None:
            return

        self.canvas.update_idletasks()

        # Get sizes
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self.current_image.size

        # Update transform
        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)

        # Apply clamped offsets
        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

        # Render image
        tk_image, data = ImageRenderer.render(
            self.canvas,
            self.current_image,
            zoom=self.transform.zoom,
            offset_x=self.transform.offset_x,
            offset_y=self.transform.offset_y,
        )
        if tk_image is None:
            return

        # Update transform again
        self.tk_image = tk_image
        canvas_w, canvas_h, img_w, img_h = data
        self.transform.update(canvas_w, canvas_h, img_w, img_h, self.zoom_factor, self.offset_x, self.offset_y)

        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

        # Persist viewport and update
        self._persist_viewport()
        self._update_scroll_visibility()

        # Draw overlays
        self._draw_selection_overlay()

    def _draw_zoom_preview(self, x0, y0, x1, y1):
        """Temporary Rectangle."""

        # Clear previous preview
        self._clear_zoom_preview()

        # Convert coordinates
        cx0, cy0 = self.transform.image_to_canvas(x0, y0)
        cx1, cy1 = self.transform.image_to_canvas(x1, y1)

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
        cx0, cy0 = self.transform.image_to_canvas(x0, y0)
        cx1, cy1 = self.transform.image_to_canvas(x1, y1)

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