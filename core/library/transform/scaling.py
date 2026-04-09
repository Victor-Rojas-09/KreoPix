import numpy as np


def compute_region_zoom_factor(canvas_w, canvas_h, img_w, img_h, x0, y0, x1, y1) -> float:
    """
    Return a zoom_factor multiplier so the selected image rectangle fits the canvas,
    relative to the default fit-to-window scale (viewport-only navigation).
    """

    rw = max(1, abs(x1 - x0))
    rh = max(1, abs(y1 - y0))
    if img_w < 1 or img_h < 1 or canvas_w < 1 or canvas_h < 1:
        return 1.0
    fit_scale = min(canvas_w / img_w, canvas_h / img_h)
    desired_scale = min(canvas_w / rw, canvas_h / rh)
    if fit_scale <= 0:
        return 1.0
    return max(0.05, desired_scale / fit_scale)


class ImageReduction:
    """
    Reduce the image resolution
    """

    def apply(self, img: np.ndarray, factor: int) -> np.ndarray:

        if factor <= 0:
            raise ValueError("The factor must be greater than 0")

        return img[::factor, ::factor]


class ImageAmplification:
    """
    Enlarge a central region of the image by
    repeating pixels.
    """

    def apply(self, img: np.ndarray, zoom_area: int, zoom_factor: int = 5) -> np.ndarray:

        h, w = img.shape[:2]

        start_row = h // 2 - zoom_area // 2
        end_row = h // 2 + zoom_area // 2

        start_col = w // 2 - zoom_area // 2
        end_col = w // 2 + zoom_area // 2

        recorte = img[start_row:end_row, start_col:end_col]

        if img.ndim == 3:
            zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor, 1)))
        else:
            zoomed = np.kron(recorte, np.ones((zoom_factor, zoom_factor)))

        return zoomed.astype(img.dtype)