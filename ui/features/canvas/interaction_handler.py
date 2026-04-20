_STROKE_TOOLS = frozenset({"brush", "eraser"})


class InteractionHandler:
    """Handles mouse and keyboard events, routing them to the controller."""

    def __init__(self, view):
        self.view = view
        self._stroke_points = []
        self._zoom_rect_start = None
        self._transform_rect_start = None
        self._transform_drag_start = None
        self._selection_start = None
        self._bind_events()

    def _bind_events(self):
        """Handles mouse and keyboard events, routing them to the controller."""

        canvas = self.view.canvas

        # Mouse events bindings
        canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        canvas.bind("<B1-Motion>", self.on_mouse_move)
        canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Mouse events for centered zoom
        canvas.bind_all("<Control-plus>", self.on_zoom_in)
        canvas.bind_all("<Control-KP_Add>", self.on_zoom_in)
        canvas.bind_all("<Control-equal>", self.on_zoom_in)
        canvas.bind_all("<Control-minus>", self.on_zoom_out)
        canvas.bind_all("<Control-KP_Subtract>", self.on_zoom_out)

        # Mouse shortcuts for the transform tool
        canvas.bind("<Return>", self.on_transform_apply)
        canvas.bind("<KP_Enter>", self.on_transform_apply)
        canvas.bind("<Escape>", self.on_transform_cancel)
        canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    # =========================================================
    # Zoom handles
    # =========================================================

    def on_zoom_in(self, event):
        """Handles zoom in."""

        if self.view.controller and self.view.controller.state.has_format():
            self.view.viewport.zoom_at_center(1.15)
        return "break"

    def on_zoom_out(self, event):
        """Handles zoom out."""

        if self.view.controller and self.view.controller.state.has_format():
            self.view.viewport.zoom_at_center(1.0 / 1.15)
        return "break"

    # =========================================================
    # Mouse Interaction
    # =========================================================

    def on_mouse_down(self, event):
        """Handle mouse events, start of action."""

        if not self.view.controller: return

        # Gives position on screen
        self.view.viewport.sync_transform()
        x, y = self.view.viewport.transform.canvas_to_image(event.x, event.y)

        tool = self.view.controller.state.current_tool

        # Tool-based behavior
        if tool in _STROKE_TOOLS:
            self._stroke_points = [(x, y)]

        elif tool == "eyedropper":
            self.view.controller.handle_eyedropper(x, y)

        elif tool == "paint_bucket":
            self.view.controller.handle_fill(x, y)

        elif tool == "select":
            self._selection_start = (x, y)
            self.view.controller.handle_rect_selection(x, y, x, y)

        elif tool == "magic_wand":
            self.view.controller.handle_magic_wand(x, y)

        elif tool == "transform":

            if self.view.controller.state.has_active_transform():
                self._transform_drag_start = (x, y)
            else:
                self._transform_rect_start = (x, y)
                self.view._draw_zoom_preview(x, y, x, y)

        elif tool == "zoom_area":
            self._zoom_rect_start = (x, y)
            self.view._draw_zoom_preview(x, y, x, y)

    def on_mouse_move(self, event):
        """Handle mouse move, while dragging."""

        if not self.view.controller: return

        self.view.viewport.sync_transform()
        tool = self.view.controller.state.current_tool

        # Only zoom area reacts
        if tool not in _STROKE_TOOLS:

            if tool == "zoom_area" and self._zoom_rect_start:

                x0, y0 = self._zoom_rect_start
                x1, y1 = self.view.viewport.transform.canvas_to_image(event.x, event.y)

                self.view._draw_zoom_preview(x0, y0, x1, y1)

            return

        x, y = self.view.viewport.transform.canvas_to_image(event.x, event.y)
        self._stroke_points.append((x, y))

        if tool == "transform":

            if self.view.controller.state.has_active_transform():

                if self._transform_drag_start is not None:

                    dx = x - self._transform_drag_start[0]
                    dy = y - self._transform_drag_start[1]

                    self._transform_drag_start = (x, y)
                    self.view.controller.update_transform(dx=dx, dy=dy)

            else:

                if self._transform_rect_start is not None:

                    x0, y0 = self._transform_rect_start
                    self.view._draw_zoom_preview(x0, y0, x, y)

    def on_mouse_up(self, event):
        """Handle mouse up, the end of action."""

        if not self.view.controller: return

        self.view.viewport.sync_transform()
        tool = self.view.controller.state.current_tool
        x, y = self.view.viewport.transform.canvas_to_image(event.x, event.y)

        # Area and selection tools
        if tool == "select" and self._selection_start:

            x0, y0 = self._selection_start

            self.view.controller.handle_rect_selection(x0, y0, x, y)
            self._selection_start = None
            return

        if tool == "zoom_area" and self._zoom_rect_start:

            x0, y0 = self._zoom_rect_start

            self.view.controller.handle_zoom_to_rect(x0, y0, x, y)
            self._zoom_rect_start = None
            self.view._clear_zoom_preview()
            return

        if tool == "transform":
            if self.view.controller.state.has_active_transform():
                self._transform_drag_start = None
            else:
                self.view._clear_zoom_preview()

                if self._transform_rect_start is not None:

                    x0, y0 = self._transform_rect_start
                    self._transform_rect_start = None

                    if abs(x - x0) < 2 and abs(y - y0) < 2:
                        return

                    self.view.controller.handle_rect_selection(x0, y0, x, y)
                    self.view.controller.start_transform_from_selection()
            return

        if tool in _STROKE_TOOLS:
            self._stroke_points.append((x, y))
            self.view.controller.handle_paint_stroke(self._stroke_points)
            self._stroke_points = []

    # =========================================================
    # Transform keyboard
    # =========================================================

    def on_transform_apply(self, event=None):
        """Commit the active transform session to the layer."""

        controller = self.view.controller

        if controller and controller.state.get_tool() == "transform" and controller.state.has_active_transform():
            controller.apply_transform()

    def on_transform_cancel(self, event=None):
        """Cancel the active transform session and restore the original pixels."""

        controller = self.view.controller

        if controller and controller.state.get_tool() == "transform" and controller.state.has_active_transform():
            controller.cancel_transform()

    def on_mouse_wheel(self, event):
        """Route mouse-wheel events."""

        controller = self.view.controller
        if not controller:
            return
        if controller.state.get_tool() == "transform" and controller.state.has_active_transform():

            scale_delta = 0.1 if event.delta > 0 else -0.1

            current_scale = controller.state.transform_session.scale

            new_scale = max(0.1, min(5.0, current_scale + scale_delta))

            controller.update_transform(scale=new_scale)