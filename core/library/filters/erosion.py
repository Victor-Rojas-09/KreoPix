import cv2
import numpy as np


class Erosion:
    """
    Apply morphological erosion to reduce white areas in an image.
    """

    def apply(self, img: np.ndarray, kernel_size: int = 3, iterations: int = 1) -> np.ndarray:

        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        eroded = cv2.erode(img, kernel, iterations=iterations)

        return eroded