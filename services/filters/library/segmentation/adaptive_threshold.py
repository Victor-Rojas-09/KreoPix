import cv2
import numpy as np


class AdaptiveThreshold:
    """
    It uses adaptive thresholding for image segmentation.
    """

    def apply(self, img: np.ndarray, block_size: int, C: int, method: str = "gaussian") -> np.ndarray:

        # Convert to grayscale if necessary
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Ensure that block_size is odd
        if block_size % 2 == 0:
            block_size += 1

        if method == "mean":
            adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
        else:
            adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C

        binary = cv2.adaptiveThreshold(
            img,
            255,
            adaptive_method,
            cv2.THRESH_BINARY,
            block_size,
            C
        )

        return binary