from core.library.transform.scaling import compute_region_zoom_factor
from ui.features.canvas.canvas_transform import CanvasTransform


class ViewportManager:
    """Manages zoom, offsets, and scrollbars for the canvas."""

    def __init__(self, view):
        self.view = view
        self.transform = CanvasTransform()

        self.zoom_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self._suppress_scroll = False

    def sync_transform(self):
        """Apply zoom_factor and offsets and clamp."""

        if self.view.current_image is None:
            return

        self.view.canvas.update_idletasks()
        cw = max(1, self.view.canvas.winfo_width())
        ch = max(1, self.view.canvas.winfo_height())
        iw, ih = self.view.current_image.size

        self.transform.update(cw, ch, iw, ih, self.zoom_factor, self.offset_x, self.offset_y)
        self.offset_x = self.transform.offset_x
        self.offset_y = self.transform.offset_y

    def zoom_at_center(self, factor_mult: float):
        """Zoom in and out keeping the canvas center on the same image pixel."""

        if self.view.current_image is None:
            return

        self.view.canvas.update_idletasks()

        # Canvas dimensions
        cw = max(1, self.view.canvas.winfo_width())
        ch = max(1, self.view.canvas.winfo_height())
        cx = cw / 2.0
        cy = ch / 2.0

        iw, ih = self.view.current_image.size

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
        self.persist_viewport()
        self.view._render_image()

    def zoom_to_rect(self, x0, y0, x1, y1):
        """Fit the given image rectangle in the viewport."""

        if self.view.current_image is None or not self.view.controller:
            return

        self.view.canvas.update_idletasks()

        cw = max(1, self.view.canvas.winfo_width())
        ch = max(1, self.view.canvas.winfo_height())
        iw, ih = self.view.current_image.size

        # Compute best zoom
        zf = compute_region_zoom_factor(cw, ch, iw, ih, x0, y0, x1, y1)

        # Clamp zoom
        self.zoom_factor = max(0.05, min(20.0, zf))
        rx0, rx1 = sorted((x0, x1))
        ry0, ry1 = sorted((y0, y1))
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
        self.persist_viewport()
        self.view._render_image()

    def handle_scroll(self, value: float, axis: str):
        """Generic handler for scroll slider movement."""

        if self._suppress_scroll or self.view.current_image is None:
            return

        # Sync transform state
        self.sync_transform()

        # Select axis-specific logic
        if axis == "x":
            min_o, max_o = self.transform.scroll_range_x()
        elif axis == "y":
            min_o, max_o = self.transform.scroll_range_y()
        else:
            raise ValueError("Invalid axis")

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
        self.persist_viewport()
        self.view._render_image()

    def update_scroll_visibility(self):
        """Update visibility and position of a single scroll slider."""

        if self.view.current_image is None:
            self.view.v_scroll.grid_remove()
            self.view.h_scroll.grid_remove()
            return

        self._update_single_scroll("x")
        self._update_single_scroll("y")

    def _update_single_scroll(self, axis: str):
        """Update the scroll position of a single scroll slider."""

        visibility_threshold = 0.5
        epsilon = 1e-6

        if axis == "x":
            min_o, max_o = self.transform.scroll_range_x()
            scroll_widget = self.view.h_scroll
            offset = self.offset_x
            grid_kwargs = dict(row=1, column=0, sticky="ew")
        else:
            min_o, max_o = self.transform.scroll_range_y()
            scroll_widget = self.view.v_scroll
            offset = self.offset_y
            grid_kwargs = dict(row=0, column=1, sticky="ns")

        if abs(max_o - min_o) > visibility_threshold:
            scroll_widget.grid(**grid_kwargs)
            denom = min_o - max_o
            if abs(denom) > epsilon:
                self._suppress_scroll = True
                try:
                    value = 100.0 * (offset - max_o) / denom
                    scroll_widget.set(value)
                finally:
                    self._suppress_scroll = False
        else:
            scroll_widget.grid_remove()

    def persist_viewport(self):
        """Persist viewport information."""

        if self.view.controller:
            self.view.controller.update_active_session_viewport(
                self.zoom_factor,
                self.offset_x,
                self.offset_y
            )

    def restore_from_session(self, session):
        """Restore viewport information."""

        self.zoom_factor = getattr(session, "zoom_factor", 1.0)
        self.offset_x = getattr(session, "offset_x", 0.0)
        self.offset_y = getattr(session, "offset_y", 0.0)

        if self.view.current_image:
            self.view._render_image()