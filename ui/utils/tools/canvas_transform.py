class CanvasTransform:
    """Handles coordinate transformations between canvas space and image space."""

    def __init__(self):

        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.img_w = 1
        self.img_h = 1

    def update(self, canvas_w, canvas_h, img_w, img_h):
        """Update transformation parameters based on canvas and image size."""

        self.img_w = img_w
        self.img_h = img_h

        self.scale = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * self.scale)
        new_h = int(img_h * self.scale)

        self.offset_x = (canvas_w - new_w) // 2
        self.offset_y = (canvas_h - new_h) // 2

    def canvas_to_image(self, cx, cy):
        """Convert canvas coordinates into image coordinates."""

        ix = int((cx - self.offset_x) / self.scale)
        iy = int((cy - self.offset_y) / self.scale)

        return (
            max(0, min(self.img_w - 1, ix)),
            max(0, min(self.img_h - 1, iy))
        )