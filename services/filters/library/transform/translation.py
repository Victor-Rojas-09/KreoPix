import numpy as np


class ImageTranslation:
    """
    Translate an image on the plane.
    """

    def apply(self, img: np.ndarray, dx: int, dy: int) -> np.ndarray:

        h, w = img.shape[:2]

        translated = np.zeros_like(img)

        x1d = max(0, dx)
        y1d = max(0, dy)

        x2d = min(w, w + dx)
        y2d = min(h, h + dy)

        x1s = max(0, -dx)
        y1s = max(0, -dy)

        x2s = x1s + (x2d - x1d)
        y2s = y1s + (y2d - y1d)

        if x2d > x1d and y2d > y1d:
            translated[y1d:y2d, x1d:x2d] = img[y1s:y2s, x1s:x2s]

        return translated