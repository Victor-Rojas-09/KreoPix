import cv2
import numpy as np


class RobertsEdge:
    """
    Detect edges in an image using the Roberts operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kx = np.array([[1, 0],
                       [0, -1]], dtype=np.float32)

        ky = np.array([[0, 1],
                       [-1, 0]], dtype=np.float32)

        gx = cv2.filter2D(gray, cv2.CV_64F, kx)
        gy = cv2.filter2D(gray, cv2.CV_64F, ky)

        edges = np.sqrt(gx**2 + gy**2)

        edges = cv2.normalize(
            edges, None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        return edges


class SobelXEdge:
    """
    Detects horizontal edges using the X-direction Sobel operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)

        sobelx = cv2.normalize(
            np.abs(sobelx), None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        return sobelx


class SobelYEdge:
    """
    Detects vertical edges using the Y-axis Sobel operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        sobely = cv2.normalize(
            np.abs(sobely), None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        return sobely


class SobelMagnitude:
    """
    Calculate the gradient magnitude using the Sobel filter.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        mag = np.sqrt(sx**2 + sy**2)

        mag = cv2.normalize(
            mag, None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        return mag


class PrewittEdge:
    """
    Detect edges using the Prewitt operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kx = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ], dtype=np.float32)

        ky = np.array([
            [1, 1, 1],
            [0, 0, 0],
            [-1, -1, -1]
        ], dtype=np.float32)

        gx = cv2.filter2D(gray, cv2.CV_64F, kx)
        gy = cv2.filter2D(gray, cv2.CV_64F, ky)

        edges = np.sqrt(gx**2 + gy**2)

        edges = cv2.normalize(
            edges, None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

        return edges


class LaplacianEdge:
    """
    Detect edges using the Laplacian operator.
    """

    def apply(self, img: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)

        lap = cv2.normalize(
            np.abs(lap), None, 0, 255, cv2.NORM_MINMAX
        ).astype(np.uint8)

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