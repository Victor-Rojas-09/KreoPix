import cv2
import numpy as np

class ImageFlip:
    """
    Flip the image horizontally, vertically, or both.
    """

    def apply(self, img: np.ndarray, mode: str = "horizontal") -> np.ndarray:

        if mode == "horizontal":
            return cv2.flip(img, 1)  # Flip horizontal

        elif mode == "vertical":
            return cv2.flip(img, 0)  # Flip vertical

        elif mode == "both":
            return cv2.flip(img, -1)  # Flip horizontal + vertical

        else:
            raise ValueError("Mode must be 'horizontal', 'vertical', or 'both'")