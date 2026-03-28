import cv2
import numpy as np


class GaussianBlur:
    """
    Apply Gaussian blur to the image to reduce noise.
    """

    def apply(self, img: np.ndarray, ksize: int) -> np.ndarray:

        if ksize % 2 == 0:
            ksize += 1

        blurred = cv2.GaussianBlur(img, (ksize, ksize), 0)

        return blurred