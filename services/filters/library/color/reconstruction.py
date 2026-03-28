import numpy as np


class RGBReconstructor:
    """
    Reconstructs an RGB image from three channels:
    red, green, and blue.
    """

    def apply(self, r: np.ndarray, g: np.ndarray, b: np.ndarray) -> np.ndarray:

        if r.shape != g.shape or r.shape != b.shape:
            raise ValueError("All channels must be the same size.")

        h, w = r.shape[:2]

        img = np.zeros((h, w, 3), dtype=r.dtype)

        img[:, :, 2] = r[:, :, 2]
        img[:, :, 1] = g[:, :, 1]
        img[:, :, 0] = b[:, :, 0]

        return img