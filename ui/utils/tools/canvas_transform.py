def screen_to_image(sx, sy, zoom, offset_x, offset_y, img_w, img_h) -> tuple[int, int]:
    """Convert canvas coordinates to image pixel indices."""

    if zoom <= 0:
        return 0, 0
    ix = (sx - offset_x) / zoom
    iy = (sy - offset_y) / zoom
    return (
        int(max(0, min(img_w - 1, ix))),
        int(max(0, min(img_h - 1, iy))),
    )


def image_to_screen(ix, iy, zoom, offset_x, offset_y) -> tuple[float, float]:
    """Convert image pixel coordinates to canvas coordinates."""

    return offset_x + ix * zoom, offset_y + iy * zoom


class CanvasTransform:
    """ Holds the active viewport: user zoom_factor, and screen-space offsets of the image origin."""

    def __init__(self):
        self.img_w = 1
        self.img_h = 1
        self._canvas_w = 1
        self._canvas_h = 1

    @property
    def canvas_w(self) -> int:
        """canvas width."""

        return self._canvas_w

    @property
    def canvas_h(self) -> int:
        """canvas height."""
        return self._canvas_h
        self.zoom_factor = 1.0
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

    def update(self, canvas_w, canvas_h, img_w, img_h, zoom_factor, offset_x, offset_y):
        """Recompute effective zoom and clamp offsets to keep the image in a valid range."""

        self.img_w = max(1, img_w)
        self.img_h = max(1, img_h)
        self._canvas_w = max(1, canvas_w)
        self._canvas_h = max(1, canvas_h)

        fit = min(canvas_w / self.img_w, canvas_h / self.img_h)
        self.zoom_factor = max(0.05, float(zoom_factor))
        self.zoom = fit * self.zoom_factor
        self.offset_x = float(offset_x)
        self.offset_y = float(offset_y)
        self._clamp_offsets()

    def _clamp_offsets(self):
        """Single pan model: only offset_x / offset_y; no separate scroll pan."""

        cw, ch = self._canvas_w, self._canvas_h
        sw = self.img_w * self.zoom
        sh = self.img_h * self.zoom

        if sw <= cw:
            self.offset_x = (cw - sw) / 2.0
        else:
            self.offset_x = max(cw - sw, min(0.0, self.offset_x))

        if sh <= ch:
            self.offset_y = (ch - sh) / 2.0
        else:
            self.offset_y = max(ch - sh, min(0.0, self.offset_y))

    def canvas_to_image(self, sx: float, sy: float) -> tuple[int, int]:
        """Convert canvas to image."""

        return screen_to_image(sx, sy, self.zoom, self.offset_x, self.offset_y, self.img_w, self.img_h)

    def image_to_canvas(self, ix: float, iy: float) -> tuple[int, int]:
        """Convert image to canvas."""

        x, y = image_to_screen(ix, iy, self.zoom, self.offset_x, self.offset_y)

        return int(round(x)), int(round(y))

    def scroll_range_x(self) -> tuple[float, float]:
        """with min_ox <= max_ox; equal if no horizontal scroll."""

        sw = self.img_w * self.zoom
        cw = self._canvas_w

        if sw <= cw:
            return self.offset_x, self.offset_x

        return cw - sw, 0.0

    def scroll_range_y(self) -> tuple[float, float]:
        """With min_oy <= max_oy; equal if no vertical scroll."""

        sh = self.img_h * self.zoom
        ch = self._canvas_h

        if sh <= ch:
            return self.offset_y, self.offset_y

        return ch - sh, 0.0
