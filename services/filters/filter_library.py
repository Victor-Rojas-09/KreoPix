import numpy as np
import cv2

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

        gray = (0.21 * img[:, :, 0] + 0.72 * img[:, :, 1] + 0.07 * img[:, :, 2])

        return np.stack((gray, gray, gray), axis=2)


class LaplacianEdge:
    """
    Detect edges using the Laplacian operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)

        lap = cv2.normalize(np.abs(lap), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        return lap


class CannyEdge:
    """
    Detects edges using the Canny algorithm.
    """

    def __init__(self, threshold1: int = 80, threshold2: int = 160):

        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, self.threshold1, self.threshold2)

        return edges

class GaussianBlur:
    """
    Apply Gaussian blur to the image to reduce noise.
    """

    def apply(self, img: np.ndarray, ksize: int=80) -> np.ndarray:

        if ksize % 2 == 0:
            ksize += 1

        blurred = cv2.GaussianBlur(img, (ksize, ksize), 0)

        return blurred