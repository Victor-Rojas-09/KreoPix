import cv2
import numpy as np


class HSVColorMask:
    """
    Generate a bitmap mask based on a color range in HSV.
    """

    def apply(self, img: np.ndarray, lower_color: tuple, upper_color: tuple) -> np.ndarray:

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array(lower_color, dtype=np.uint8)
        upper = np.array(upper_color, dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)

        return mask

class ApplyMask:
    """
    Apply a bitmap mask to an image.
    """

    def apply(self, img: np.ndarray, mask: np.ndarray) -> np.ndarray:
        segmented = cv2.bitwise_and(img, img, mask=mask)

        return segmented