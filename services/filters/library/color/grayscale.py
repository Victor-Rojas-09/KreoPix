import numpy as np


class GrayscaleAverage:
    """
    Convert an image to grayscale using
    the averaging method.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = np.mean(img, axis=2)

        return np.stack((gray, gray, gray), axis=2)


class GrayscaleLuminosity:
    """
    Convert an image to grayscale using
    the luminance method.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = (
            0.21 * img[:, :, 0] +
            0.72 * img[:, :, 1] +
            0.07 * img[:, :, 2]
        )

        return np.stack((gray, gray, gray), axis=2)


class GrayscaleMidgray:
    """
    Convert an image to grayscale using
    the Midgray method.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:
        gray = (np.max(img, axis=2) + np.min(img, axis=2)) / 2

        return np.stack((gray, gray, gray), axis=2)