import tkinter as tk

from ui.utils.tools.window_positioner import WindowPositioner


class HistogramCurvesDialog(tk.Toplevel):
    """Histogram display with editable master RGB curve and live preview."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.title("Histogram & Curves")
        self.resizable(False, False)

        try:
            self.iconbitmap("assets/app/LOGO.ico")
        except tk.TclError:
            pass

        self._hist_w = 356
        self._hist_h = 220
        self._pad = 12
        self._canvas_w = self._hist_w + self._pad * 2
        self._canvas_h = self._hist_h + self._pad * 2

        WindowPositioner.center_to_parent(self, parent, self._canvas_w + 48, self._canvas_h + 220)

        self.transient(parent)
        self.grab_set()

        layer = self.controller.state.get_selected_layer()
        if not layer:
            self.destroy()
            return

        self._snapshot = layer.image.copy()
        self._points: list[tuple[int, int]] = [(0, 0), (255, 255)]
        self._drag_index: int | None = None
        self._after_id = None

        self._build()

    # ==========================================================
    # UI
    # ==========================================================

    def _build(self):
        outer = tk.Frame(self, bg="#2b2b2b")
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg="#2b2b2b")
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="Histogram & curves",
            font=("Segoe UI", 14, "bold"),
            bg="#2b2b2b",
            fg="#f0f0f0",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Drag points. Double-click curve to add; double-click point to remove (endpoints fixed).",
            font=("Segoe UI", 8),
            bg="#2b2b2b",
            fg="#aaaaaa",
            wraplength=self._canvas_w + 20,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        self._canvas = tk.Canvas(
            outer,
            width=self._canvas_w,
            height=self._canvas_h,
            bg="#1e1e1e",
            highlightthickness=0,
        )
        self._canvas.pack(padx=20, pady=8)

        self._canvas.bind("<Button-1>", self._on_press)
        self._canvas.bind("<B1-Motion>", self._on_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_release)
        self._canvas.bind("<Double-Button-1>", self._on_double_click)

        btn_row = tk.Frame(outer, bg="#2b2b2b")
        btn_row.pack(fill="x", padx=20, pady=(8, 16))

        tk.Button(
            btn_row,
            text="OK",
            bg="#505050",
            fg="white",
            activebackground="#606060",
            padx=14,
            pady=4,
            command=self._on_ok,
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            btn_row,
            text="Cancel",
            bg="#505050",
            fg="white",
            activebackground="#606060",
            padx=14,
            pady=4,
            command=self._on_cancel,
        ).pack(side="right")

        self._redraw_all()

    # ==========================================================
    # Coordinate mapping
    # ==========================================================

    def _chart_rect(self):
        x0 = self._pad
        y0 = self._pad
        x1 = x0 + self._hist_w
        y1 = y0 + self._hist_h
        return x0, y0, x1, y1

    def _img_to_canvas(self, ix: int, iy: int) -> tuple[float, float]:
        x0, y0, x1, y1 = self._chart_rect()
        cx = x0 + (ix / 255.0) * (x1 - x0)
        cy = y1 - (iy / 255.0) * (y1 - y0)
        return cx, cy

    def _canvas_to_img(self, cx: float, cy: float) -> tuple[int, int]:
        x0, y0, x1, y1 = self._chart_rect()
        w = x1 - x0
        h = y1 - y0
        if w <= 0 or h <= 0:
            return 0, 0
        ix = int(round((cx - x0) / w * 255))
        iy = int(round((y1 - cy) / h * 255))
        return max(0, min(255, ix)), max(0, min(255, iy))

    # ==========================================================
    # Drawing
    # ==========================================================

    def _redraw_all(self):
        self._canvas.delete("all")
        x0, y0, x1, y1 = self._chart_rect()
        self._canvas.create_rectangle(x0, y0, x1, y1, outline="#444444", width=1)

        layer = self.controller.state.get_selected_layer()
        if not layer:
            return

        data = self.controller.get_histogram_for_image(layer.image)
        max_c = max(data["max_count"], 1)
        luma = data["luma"]

        for i in range(256):
            h = (float(luma[i]) / max_c) * self._hist_h
            bx0 = x0 + i * (self._hist_w / 256.0)
            bw = max(1.0, self._hist_w / 256.0)
            self._canvas.create_rectangle(
                bx0, y1 - h, bx0 + bw, y1, fill="#4a4a4a", outline="", width=0
            )

        pts = sorted(self._points, key=lambda p: p[0])
        for i in range(len(pts) - 1):
            x_a, y_a = self._img_to_canvas(pts[i][0], pts[i][1])
            x_b, y_b = self._img_to_canvas(pts[i + 1][0], pts[i + 1][1])
            self._canvas.create_line(x_a, y_a, x_b, y_b, fill="#e0c040", width=2)

        for i, (ix, iy) in enumerate(pts):
            cx, cy = self._img_to_canvas(ix, iy)
            r = 5
            fill = "#ffd54f" if i in (0, len(pts) - 1) and len(pts) > 1 else "#ffecb3"
            self._canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=fill, outline="#333")

    # ==========================================================
    # Interaction
    # ==========================================================

    def _hit_index(self, cx: float, cy: float):
        pts = sorted(self._points, key=lambda p: p[0])
        for i, (ix, iy) in enumerate(pts):
            px, py = self._img_to_canvas(ix, iy)
            if (cx - px) ** 2 + (cy - py) ** 2 <= 8 ** 2:
                return i
        return None

    def _on_press(self, event):
        idx = self._hit_index(event.x, event.y)
        if idx is not None:
            self._drag_index = idx
            return
        self._drag_index = None

    def _on_drag(self, event):
        if self._drag_index is None:
            return
        pts = sorted(self._points, key=lambda p: p[0])
        ix, iy = self._canvas_to_img(event.x, event.y)
        i = self._drag_index
        if i == 0:
            ix = 0
        elif i == len(pts) - 1:
            ix = 255
        else:
            prev_x = pts[i - 1][0]
            next_x = pts[i + 1][0]
            ix = max(prev_x + 1, min(next_x - 1, ix))

        pts[i] = (ix, iy)
        self._points = sorted(pts, key=lambda p: p[0])
        self._schedule_preview()

    def _on_release(self, event):
        self._drag_index = None

    def _on_double_click(self, event):
        cx, cy = event.x, event.y
        idx = self._hit_index(cx, cy)
        pts = sorted(self._points, key=lambda p: p[0])
        if idx is not None:
            if idx in (0, len(pts) - 1):
                return
            pts.pop(idx)
            self._points = sorted(pts, key=lambda p: p[0])
            self._schedule_preview()
            self._redraw_all()
            return

        ix, iy = self._canvas_to_img(cx, cy)
        if ix <= 0 or ix >= 255:
            return

        for i in range(len(pts) - 1):
            x0, _ = pts[i]
            x1, _ = pts[i + 1]
            if x0 < ix < x1:
                pts.append((ix, iy))
                self._points = sorted(pts, key=lambda p: p[0])
                self._schedule_preview()
                self._redraw_all()
                return

    def _schedule_preview(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(30, self._do_preview)

    def _do_preview(self):
        self._after_id = None
        self.controller.request_histogram_curve_preview(self._snapshot, list(self._points))
        self._redraw_all()

    def _on_ok(self):
        layer = self.controller.state.get_selected_layer()
        if layer:
            final_img = layer.image.copy()
            self.controller.request_histogram_curve_commit(self._snapshot, final_img)
        self.grab_release()
        self.destroy()

    def _on_cancel(self):
        self.controller.request_histogram_curve_cancel(self._snapshot)
        self.grab_release()
        self.destroy()
