import cv2
import numpy as np

from Image_Manager.segmentation.threshold import ImageBinarization


class ContourDetector:
    """
    Detects contours in a binary image.
    """

    def apply(self, img: np.ndarray, threshold: int = None, draw: bool = True):

        # Convert to grayscale if necessary
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        # If a threshold is provided, binarize
        if threshold is not None:
            binarizer = ImageBinarization()
            binary = binarizer.apply(gray, threshold)
        else:
            binary = gray


        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        output_img = None

        if draw:

            if img.ndim == 2:
                output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            else:
                output_img = img.copy()

            cv2.drawContours(output_img, contours, -1, (0, 255, 0), 2)

        return contours, output_img